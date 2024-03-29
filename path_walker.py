from functools import partial, reduce
import hashlib
from pathlib import Path
from os import scandir
from os.path import relpath
from sys import maxsize
from pytz import utc
from . import temp_files
from .archieve_viewer import ArchiveFactory, Archive, PasswordRequiredError, WrongPasswordError
from .caching.cache import DeniedOperationException
from typing import Callable, Iterable, Iterator
from main.api.rest_serializers import TempFileSerializer
from queue import LifoQueue, Queue
from django.conf import settings
from datetime import datetime
import itertools
import logging
import tempfile

logger = logging.getLogger(__name__)
class fake:
    def info(*args, **kwargs):
        pass
    
logger = fake
cache = temp_files.get_cache()

default_repository_path = settings.AVI_MAIN['PATHS']['default_repository_path']
default_temporary_path = settings.AVI_MAIN['PATHS']['default_temporary_path']
default_users_path = settings.AVI_MAIN['PATHS']['default_users_path']
default_common_storage_path = settings.AVI_MAIN['PATHS']['default_common_storage_path']
default_download_path = settings.AVI_MAIN['PATHS']['default_download_path']
default_upload_path = settings.AVI_MAIN['PATHS']['default_upload_path']
root_id = settings.AVI_MAIN['JS_TREE']['root_id']

class PasswordRequiredForExtract(LookupError):
    ''' Raised when required password for unpacking archive is not found. '''
    def __init__(
            self,
            archive_name:str,
            virtual_path_depth:int,
            inner_error_message:str,
            *args: object
        ) -> None:

        super().__init__(*args)
        self.archive_name = archive_name
        self.virtual_path_depth = virtual_path_depth
        self.inner_error_message = inner_error_message


class InodeCodedPathSerializer:
    @staticmethod
    def convert_path_to_inode_list(parent_path:Path, path:Path):
        def search_inode_by_component(parent_path:Path, name):
            for node in scandir(parent_path):
                if str(node.name) == name:
                    return str(node.inode())
            return None
        
        assert isinstance(parent_path, Path), f'Parent path {parent_path} is not a pathlib.Path object.'
        if not parent_path.exists():
            raise ValueError(f'Parent path {parent_path} not exists.')

        assert isinstance(path, Path), f'Path {path} is not a pathlib.Path object.'
        assert path.is_relative_to(parent_path), f'Parent path {parent_path} is not contains a path {path}.'
        if not path.exists():
            raise ValueError(f'Path {path} not exists')
        
        result = ['root']
        path = path.relative_to(parent_path)
        for node in path.parts:
            current_path = search_inode_by_component(parent_path, node)
            if current_path:
                parent_path /= node
                result.append(current_path)

        return result

    @staticmethod
    def convert_inode_list_to_path(parent_path:Path, inode_list):
        def search_component_by_inode(parent_path:Path, inode):
            if inode == root_id:
                return parent_path
            else:
                for node in scandir(parent_path):
                    if str(node.inode()) == inode:
                        return Path(node.path)
                return None
        
        assert isinstance(parent_path, Path), f'Parent path {parent_path} is not a pathlib.Path object.'
        if not parent_path.exists():
            raise ValueError(f'Parent path {parent_path} not exists.')
        
        path = parent_path
        for node in inode_list:
            current_path = search_component_by_inode(path, node)
            if _is_safe_path(current_path, parent_path):
                path = current_path
        
        return path

def get_user_root_path(user_name, *, is_download_or_upload=True):
    if user_name:
        _path = default_users_path / user_name / (default_download_path if is_download_or_upload else default_upload_path)
        return _path if Path.exists(_path) else None

def _is_safe_path(path:Path, *limiting_paths:Path):
    '''A path is safe if it is a hard link, or a symbolic link of a subfolder of each of the limiting_paths, or is not a Posix link.'''

    def check_exists_paths(*paths):
        return all([path.exists() for path in paths])

    paths = path, *limiting_paths
    paths = [Path(aisle) for aisle in paths]

    if not check_exists_paths(*paths):
        return False
    
    paths = [aisle.resolve() for aisle in paths]
    
    if not check_exists_paths(*paths):
        return False
    
    if not all([paths[0].is_relative_to(aisle) for aisle in paths[1::]]):
        return False
    
    return True

def reversed_parents(path:Path):
    components = path.parts
    prefix = Path()
    for component in components:
        prefix /= component
        yield prefix

def slice_path(path:Path, start:int=None, stop:int=None):
    # return type is pathlib.Path.
    return reduce(
        lambda left, right: left / right,
        path.parts[start:stop],
        Path()
    )

def try_parse_int(value, base=10):
    try:
        return int(value, base)
    except ValueError:
        return None

def browse_virtual_path(root_path:Path, virtual_path:Path, get_archive_pass_hook:Callable[[str], str]):
    # 2^10 - это количество уровней вложенности архива
    # Вы правда хотите использовать архивы более глубокой вложенности?
    tasks_queue = Queue(1024)
    hot_temp_file_names_queue = Queue(1024)

    def create_and_add_task(parent_path:Path, virtual_path_start:int, is_fs_or_arch_layer:bool=True):
        task = partial(
            resolve_file_system_layer if is_fs_or_arch_layer else resolve_archive_layer,
            parent_path,
            virtual_path_start
        )

        tasks_queue.put(task)

    def resolve_file_system_layer(parent_path:Path, virtual_path_start:int):
        logger.info(f'resolve_file_system_layer CALLED!!!')
        logger.info(f'parent_path: {parent_path}')
        logger.info(f'virtual_path_start: {virtual_path_start}')
        logger.info(f'virtual_path: {virtual_path}')
        sliced_virtual_path = slice_path(virtual_path, virtual_path_start)
        logger.info(f'sliced_virtual_path: {sliced_virtual_path}')
        
        def browse_while_exists():
            index:int = 0
            result:bool = False
            # TODO: Use dichotomy and do it faster. Now is O(n).
            for aisle in reversed_parents(sliced_virtual_path):
                entry = parent_path / aisle
                if entry.exists():
                    index += 1
                    continue
                else:
                    break
            else:
                # All virtual path is browsed
                result = True
                return (result, index)
            
            # (index + 1) of sliced_virtual_path does not exists
            result = False
            return (result, index)

        def browse_catalog(catalog_path):
            for node in scandir(catalog_path):
                node_path = Path(node.path)
                is_folder = node_path.is_dir() 
                if _is_safe_path(node_path, Path(catalog_path)):
                    yield {
                        'id': node.inode(),
                        'path': relpath(node_path, parent_path),
                        'name': node.name,
                        'is_directory': is_folder,
                        'has_child': is_folder and any(scandir(node_path)) or Archive.is_archive(node_path)
                    }

        is_all_virtual_path_browsed, index = browse_while_exists()
        target_path = parent_path / slice_path(virtual_path, virtual_path_start, index)
        if Archive.is_archive(target_path): # maybe this is archive?
            create_and_add_task(
                target_path,
                virtual_path_start + index,
                is_fs_or_arch_layer=False
            )
            # wait task
            return
        
        else: # is not archive
            if is_all_virtual_path_browsed:
                if target_path.is_dir():
                    yield from browse_catalog(target_path)
                    return
                else:
                    # virual path is single file (no nested entries)
                    return
                
            else:
                # virual path is broken
                return

    def resolve_archive_layer(parent_path:Path, virtual_path_start:int):
        logger.info(f'resolve_archive_layer CALLED!!!')
        logger.info(f'parent_path: {parent_path}')
        logger.info(f'virtual_path_start: {virtual_path_start}')
        logger.info(f'virtual_path: {virtual_path}')

        archive = ArchiveFactory.create_archive(parent_path)
        sliced_virtual_path = slice_path(virtual_path, virtual_path_start)
        logger.info(f'sliced_virtual_path: {sliced_virtual_path}')
        tree = archive.list_files()

        def browse_while_exists(tree):
            result:bool = False
            indexed_path = []
            # TODO: Use dichotomy and do it faster. Now is O(n).
            for aisle in reversed_parents(sliced_virtual_path):
                part:str = aisle.parts[-1]
                part_index:int = try_parse_int(part)
                try:
                    assert part_index >= 0, 'Path part must be greater than or equal to 0.'
                    tree = tree[part_index]
                    indexed_path.append(part_index)
                    continue
                except AssertionError:
                    # virual path is broken
                    return
                except IndexError:
                    break
            else:
                # All virtual path is browsed
                result = True
                return (result, tree, indexed_path)

            # (tree[part_index]) of sliced_virtual_path does not exists
            result = False
            return (result, tree, indexed_path)
        
        def browse_catalog(tree, indexed_path):
            for i, entry in enumerate(tree.data):
                yield {
                    'id': i,
                    'path': slice_path(virtual_path, 0, virtual_path_start) / intermediate_path / str(i),
                    'name':entry.file_path.name,
                    'is_directory': entry.is_dir,
                    # Realtime check
                    'has_child': True
                }

            return
        
        def extract_in_temp_file(id, nested_path, virtual_path_depth):
            logger.info('Extract in tempfile')
            logger.info(f'id = {id}')
            logger.info( f'nested_path = {nested_path}')

            def register_temp_file(output:Path):
                try:
                    cache.alloc(output_path, force=False)

                except DeniedOperationException:
                    # cache is not available (maybe is overflow?)
                    # use "hot" temp file
                    # (guaranteed to be deleted immediately after use)
                    hot_temp_file_names_queue.put(output.relative_to(default_temporary_path))
            
            try:
                cache_entry:Path = cache.get(id, force=False)
            except DeniedOperationException: # cache entry is not available
                # extract file in temp_directory
                year_month = Path(datetime.utcnow().replace(tzinfo=utc).strftime('%Y-%m'))
                output_dir: Path = default_temporary_path / year_month
                output_dir.mkdir(parents=True, exist_ok=True)
                output_path = output_dir / str(id)
                inner_error_message = ''

                try:
                    logger.info('TEST -1')
                    archive.extract_file(nested_path, output_path)
                except PasswordRequiredError as pre:
                    # password required
                    if pre.__context__:
                        inner_error_message = str(pre.__context__)
                    else:
                        inner_error_message = str(pre)
                    
                    password = None
                    archive_name = Path(archive.file_path).name
                    try:
                        password = get_archive_pass_hook(id)
                        logger.info(f'password = {password}')
                        logger.info('TEST 0')
                        archive.extract_file(nested_path, output_path, password)

                    except KeyError as ke:
                        logger.info('TEST 1')
                        # password not found
                        if ke.__context__:
                            inner_error_message = str(ke.__context__)
                        else:
                            inner_error_message = str(ke)
                        
                        raise PasswordRequiredForExtract(
                            archive_name,
                            virtual_path_depth,
                            inner_error_message,
                            'Требуется пароль для распаковки архива.'
                        )
                    
                    except WrongPasswordError as wpe:
                        logger.info('TEST 2')
                        # password is wrong
                        if wpe.__context__:
                            inner_error_message = str(wpe.__context__)
                        else:
                            inner_error_message = str(wpe)

                        raise PasswordRequiredForExtract(
                            archive_name,
                            virtual_path_depth,
                            inner_error_message,
                            'Ранее введённый пароль не подходит для архива.'
                        )
                    
                    else:
                        # password has been used
                        return output_path / nested_path
                finally:
                    # temporary file may have been created
                    register_temp_file(output_path)
                
                return output_path / nested_path
                logger.info('UEXPECTED RETURN')
            else:
                # cache has been used
                return cache_entry / nested_path
        
        def get_temp_file_id(path):
            sha256 = hashlib.sha3_256()
            sha256.update(bytes(str(path), encoding='utf-8'))
            return sha256.hexdigest()
        
        def make_intermediate_path(indexed_path):
            return reduce(
                lambda left, right: left / right,
                map(
                    lambda indx: str(indx),
                    indexed_path
                ),
                Path()
            )

        is_all_virtual_path_browsed, tree, indexed_path = browse_while_exists(tree)
        intermediate_path = make_intermediate_path(indexed_path)
        
        if is_all_virtual_path_browsed and tree.is_dir:
            yield from browse_catalog(tree, indexed_path)
            return
        else:
            # maybe this is a nested archive?
            temp_file_virtual_path = slice_path(virtual_path, 0, virtual_path_start) # / intermediate_path
            logger.info(f'temp_file_virtual_path = "{temp_file_virtual_path}"')
            temp_file_id = get_temp_file_id(temp_file_virtual_path)
            indexed_path_length = len(indexed_path)
            temp_file_path = extract_in_temp_file(temp_file_id, tree.file_path, virtual_path_start)

            create_and_add_task(
                parent_path = temp_file_path,
                virtual_path_start = virtual_path_start + indexed_path_length,
                is_fs_or_arch_layer = True
            )

            # wait task
            return

    def rm_tree(path:Path):
        ''' Remove file system tree. O(N) '''
        def handle_file(file_path:Path):
            if file_path.is_dir():
                file_path.rmdir()
            else:
                file_path = file_path.absolute()
                resolved_path = file_path
                max_reqursion = 65536# 2**16 # 65536
                if file_path.is_symlink():
                    count = 0
                    while resolved_path.is_symlink() and count <= max_reqursion:
                        logger.info('Recursion')
                        resolved_path = resolved_path.resolve()
                        count += 1
                        if count > max_reqursion:
                            raise RecursionError(f'Symlink [{file_path}] raise reqursion error.')
                
                    if resolved_path.is_relative_to(file_path):
                        resolved_path.unlink(missing_ok=True)
                else:
                    file_path.unlink(missing_ok=True)
        
        queue = Queue()
        stack = LifoQueue()
        queue.put(path)

        # Grab all file-like objects. Directories - first.
        while not queue.empty():
            entry:Path = queue.get()
            stack.put(entry)
            if entry.is_dir():
                for nested_entry in entry.iterdir():
                    queue.put(nested_entry)
        
        # Handle file-like objects
        while not stack.empty():
            entry:Path = stack.get()
            handle_file(entry)

    create_and_add_task(
        parent_path=root_path,
        virtual_path_start=0,
        is_fs_or_arch_layer=True
    )

    try:
        # resolves layers without recursion
        while not tasks_queue.empty():
            task = tasks_queue.get()
            # return iterator of file system object dictionaries
            yield from task()
        logger.info('All tasks done')
    finally:
        # remove all created hot temporary files
        while not hot_temp_file_names_queue.empty():
            relative_temp_file_name:Path = hot_temp_file_names_queue.get()
            root_relative_temp_file_name : Path = default_temporary_path / relative_temp_file_name.parts[0]
            temp_file_name = default_temporary_path / relative_temp_file_name
            rm_tree(temp_file_name)
            
            # remove year_month folder if empty
            if root_relative_temp_file_name.exists() and \
                not any(scandir(root_relative_temp_file_name)):
                rm_tree(root_relative_temp_file_name)
