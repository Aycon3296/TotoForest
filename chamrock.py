import _collections_abc
from bisect import bisect_left, bisect_right, insort_left
from functools import partial, update_wrapper
from sys import maxsize
import logging

logger = logging.getLogger(__name__)

__all__= ['Shamrock']

class NoneElement(Exception):
    ''' This class represents an spetial element that should never be
        in an instance of this collection. Do not use this.'''

class Shamrock(_collections_abc.MutableSequence):
    ''' Represent list-like tree. '''

    def __init__(self, item, initlist=None, change_length=None, change_is_sorted=None):
        self.__dict__['item'] = item
        self.__dict__['data'] = []
        self.__dict__['length'] = 0
        self.__dict__['_change_length_hook_list'] = [change_length] if change_length is not None else []
        self.__dict__['is_sorted'] = True
        self.__dict__['_change_is_sorted_hook_list'] = [change_is_sorted] if change_is_sorted is not None else []
        self.__dict__['_guaranteed_change_length'] = partial(self._guaranteed, after_func=self._change_length)
        self.__dict__['_guaranteed_change_is_sorted'] = partial(self._guaranteed, after_func=self._change_is_sorted)

        if initlist is not None:
            # XXX should this accept an arbitrary sequence?
            procedure = None

            if type(initlist) == type(self.data):
                def procedure():
                    self.__dict__['data'][:] = initlist
                    self.__dict__['length'] += len(initlist)
            elif isinstance(initlist, __class__):
                def procedure():
                    self.__dict__['data'][:] = initlist.data[:]
                    self.__dict__['length'] += len(initlist)
            else:
                def procedure():
                    listed = list(initlist)
                    self.__dict__['data'] = listed
                    self.__dict__['length'] += len(list(initlist))
            
            if procedure is not None:
                self._guaranteed_change_length(procedure)(len(initlist))

    def _subscribe(self, *items, force=False):
        for entry in items:
            if isinstance(entry, __class__):
                if self._change_length not in entry._change_length_hook_list or force:
                    entry._change_length_hook_list.append(self._change_length)
                if self._change_is_sorted not in entry._change_is_sorted_hook_list or force:
                    entry._change_is_sorted_hook_list.append(self._change_is_sorted)
                yield entry
            else:
                yield entry

    def _unsubscribe(self, *items, force=False):
        for entry in items:
            if isinstance(entry, __class__):
                if force or self._change_length in entry._change_length_hook_list:
                    entry._change_length_hook_list.remove(self._change_length)
                if force or self._change_is_sorted in entry._change_is_sorted_hook_list:
                    entry._change_is_sorted_hook_list.remove(self._change_is_sorted)
                yield entry
            else:
                yield entry

    def _guaranteed(self, before_func, *args, after_func, **kwds):
        def guaranteed_wrapper(*_args, **_kwds):
            result = None
            try:
                result = before_func(*args, **kwds)
            except:
                raise
            else:
                after_func(*_args, **_kwds)
                return result
        
        return guaranteed_wrapper

    def _change_length(self, cnt:int=1, ml:int=1):
            self.__dict__['length'] += cnt * ml
            for hook in self._change_length_hook_list:
                hook(cnt, ml)
    
    def _change_is_sorted(self, is_sorted:bool=False):
        self.__dict__['is_sorted'] = is_sorted
        for hook in self._change_is_sorted_hook_list:
            hook(is_sorted)
    
    def _product_or_get(self, *items):
        for entry in items:
            if isinstance(entry, __class__):
                yield entry
            else:
                yield self.__class__(entry)                
    
    def __getattr__(self, attr):
        return getattr(self.item, attr)
    
    def __setattr__(self, attr, value):
        setattr(self.item, attr, value)
    
    def __delattr__(self, attr):
        delattr(self.item, attr)

    def __repr__(self):
        return repr(self.item)

    def __lt__(self, other):
        return self.item < self.__cast(other)

    def __le__(self, other):
        return self.item <= self.__cast(other)

    def __eq__(self, other):
        return self.item == self.__cast(other)

    def __gt__(self, other):
        return self.item > self.__cast(other)

    def __ge__(self, other):
        return self.item >= self.__cast(other)

    def __cast(self, other):
        return other.item if isinstance(other, __class__) else other
    
    def __get_index(self, item, start=0, stop=maxsize):
        stop = min(len(self.data), stop)
        if isinstance(item, __class__):
            if self.is_sorted:
                index = bisect_left(self.data, item, start, stop)
                return index if index < len(self.data) and self.data[index].item == item else -1
            else:
                return next([i for i, entry in enumerate(self.data[start:stop]) if entry == item], -1)
        else:
            mapped = list(map(lambda entry: entry.item, self.data[start:stop]))
            if self.is_sorted:
                index = bisect_left(mapped, item)
                return index if index < len(self.data) and self.data[index].item == item else -1
            else:
                return next([i for i, entry in enumerate(mapped) if entry == item], -1)

    def __contains__(self, item):
        return self.__get_index(item) != -1

    def __len__(self):
        return self.length

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    def __setitem__(self, i, item):
        length = 0
        
        def procedure():
            try:
                self._unsubscribe(self.data[i])
                length -= len(self.data[i])
            except IndexError:
                pass
            finally:
                self.data[i] = next(self._subscribe(*self._product_or_get(item)))
                length += len(self.data[i])
            
        self._guaranteed_change_is_sorted(procedure)(length)

    def __delitem__(self, i):
        length = len(self.data[i])
        def procedure():
            self._unsubscribe(self.data[i])
            del self.data[i]

        self._guaranteed_change_length(procedure)(-length)
        

    def __add__(self, other):
        product = None
        if isinstance(other, __class__):
            product = next(self._product_or_get(self.data + other.data))
        
        elif isinstance(other, type(self.data)):
            product = next(self._product_or_get(self.data + other))
        
        else:
            product = next(self._product_or_get(self.data + list(other)))
        
        self._unsubscribe(*product.data)
        return product
    
    def __radd__(self, other):
        product = None

        if isinstance(other, __class__):
            product = next(self._product_or_get(other.data + self.data))
        
        elif isinstance(other, type(self.data)):
            product = next(self._product_or_get(other + self.data))
        else:
            product = next(self._product_or_get(list(other) + self.data))
        
        self._unsubscribe(*product.data)
        return product

    def __iadd__(self, other):
        if isinstance(other, __class__):
            def procedure():
                for entry in self._subscribe(*self._product_or_get(*other.data)):
                    self.__dict__['data'] += entry
            
            self._guaranteed_change_is_sorted(
                self._guaranteed_change_length(procedure),
                len(other)
            )()

        elif isinstance(other, type(self.data)):
            def procedure():
                for entry in self._subscribe(*self._product_or_get(*other)):
                    self.__dict__['data'] += entry
            
            self._guaranteed_change_is_sorted(
                self._guaranteed_change_length(procedure),
                len(other)
            )()
        else:
            listed = list(other)
            def procedure():
                for entry in self._subscribe(*self._product_or_get(*listed)):
                    self.__dict__['data'] += entry

            self._guaranteed_change_is_sorted(
                self._guaranteed_change_length(procedure),
                len(listed)
            )()

        return self

    def __mul__(self, n):
        assert isinstance(n, int), 'Cannot multiply by anything other than an integer'
        product = next(self._product_or_get(self.data * n))
        self._unsubscribe(*product.data)
        return product

    __rmul__ = __mul__

    def __imul__(self, n):
        def procedure():
            self.data *= n
        
        self._guaranteed_change_is_sorted(
            self._guaranteed_change_length(procedure),
            ml=(n - 1) * len(self)
        )()

        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)

        # Create a copy and avoid triggering descriptors
        data = self.__dict__["data"][:]
        for entry in data:
            inst.__dict__["_subscribe"](entry)
        
        inst.__dict__["data"] = data
        return inst

    def append(self, item):
        def procedure():
            product = next(self._subscribe(*self._product_or_get(item)))
            self.data.append(product)

        self._guaranteed_change_is_sorted(
            self._guaranteed_change_length(procedure)
        )()

    def insert(self, i, item):
        def procedure():
            product = next(self._subscribe(*self._product_or_get(item)))
            self.data.insert(i, product)

        self._guaranteed_change_is_sorted(
            self._guaranteed_change_length(procedure)
        )()
    
    def insert_sorted(self, item, force=False):
        def procedure():
            product = next(self._subscribe(*self._product_or_get(item)))
            if self.is_sorted:
                index = bisect_left(self.data, product)
                insort_left(self.data, product)
                return index
            else:
                if not force:
                    raise ValueError('The collection is not sorted!')
                else:
                    self.data.append(product)
                    return len(self.data) - 1
        
        return self._guaranteed_change_length(procedure)()

    def pop(self, i=-1):
        return next(self._unsubscribe(self._guaranteed_change_length(self.data.pop, i)(-1)))

    def remove(self, item):
        index = self.__get_index(item)
        if index >= 0:
            def procedure():
                buffer = self.data[index]
                self._unsubscribe(buffer)
                self.data.remove(self.data[index])

            self._guaranteed_change_length(procedure)(-1)
        else:
            # Delegating raising error
            self.data.remove(NoneElement)

    def clear(self):
        def procedure():
            self._unsubscribe(*self.data)
            self.data.clear()

        self._guaranteed_change_is_sorted(
            self._guaranteed_change_length(procedure),
            -len(self)
        )(True)

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        if isinstance(item, __class__):
            if self.is_sorted:
                return bisect_right(self.data, item) - bisect_left(self.data, item)
            else:
                return self.data.count(item)
        else:
            mapped = list(map(lambda entry: entry.item, self.data))

            if self.is_sorted:
                return bisect_right(mapped, item) - bisect_left(mapped, item)
            else:
                return mapped.count(item)

    def index(self, item, *args):
        index = self.__get_index(item, *args)
        if index < 0:
            # Delegating raising error
            return self.data.index(NoneElement)
        else:
            return index

    def reverse(self):
        def procedure():
            self.data.reverse()

        self._guaranteed_change_is_sorted(procedure)(len(self.data) > 0)

    def sort(self, /, *args, **kwds):
        self._guaranteed_change_is_sorted(
            self.data.sort,
            *args,
            **kwds
        )(True)

    def extend(self, other):
        def procedure():
            products = self._subscribe(self._product_or_get(*other))                
            self.data.extend(products)

        self._guaranteed_change_is_sorted(
            self._guaranteed_change_length(procedure),
            len(other)
        )()
