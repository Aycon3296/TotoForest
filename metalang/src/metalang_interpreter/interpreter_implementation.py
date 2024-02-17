from enum import Enum
from metalang_interpreter.conf import settings

commands = ['><+-[].,']

class InterpreterMode(Enum):
    default = 0
    debug = 1

class InterpreterError(ValueError):
    ''' Interpreter in incorrect state. '''
    
    def __init__(self, message, *args: object) -> None:
        message = f'Incorrect interpreter state. {message}'
        super().__init__(message, *args)

class InterpreterState():
    def __init__(self):
        self.memory = []
        self._pointer = 0
    
    def initialState(self):
        return self
    
    def go_to_left(self):
        if self._pointer <= 0:
            raise ValueError('Pointer less or equal to 0.')
        else:
            self._pointer -= 1
            return self
    
    def go_to_right(self):
        if self._pointer <= 0:
            raise ValueError('Pointer less or equal to 0.')
        else:
            self._pointer -= 1
            return self
    

class Interpreter:
    def __init__(self, mode:InterpreterMode = InterpreterMode(settings.default_mode)):
        self._mode = mode
        self._state: InterpreterState = InterpreterState.initialState()
    
    @property
    def mode(self):
        return self._mode
    
    @mode.setter
    def mode(self, mode):
        self._mode = mode
    
    def run(self, initial_code:str):
        [print(cmd) for cmd in initial_code]
    