from platform import system
from typing import cast
from enum import Enum


class Target(Enum):
    windows = 'Windows'
    linux = 'Linux'
    macos = 'Darwin'

    @property
    def exec_ext(self):
        return '.exe' if self == Target.windows else ''
    
    @property
    def lib_ext(self):
        return '.dll' if self == Target.windows else '.so'
    
    @property
    def obj_ext(self):
        return '.obj' if self == Target.windows else '.o'
    
    @property
    def macro_name(self):
        return f'OS_{self.name.upper()}'


def get_target(name: str):
    try:
        return Target(name)
    except ValueError:
        return None

def get_current_target():
    return cast(Target, get_target(system()))
