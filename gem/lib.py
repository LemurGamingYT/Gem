from typing import Optional, cast, Union, Any
from dataclasses import dataclass
from logging import info

from llvmlite import ir as lir

from gem.c_registry import CRegistry
from gem import ir


class UnknownFunctionError(BaseException):
    pass

class InvalidArgumentError(BaseException):
    pass


def function(self, ret_type: Optional[ir.Type] = None, params: Optional[list[ir.Param]] = None,
            flags: Optional[ir.FunctionFlags] = None, override_name: Optional[str] = None):
    if ret_type is None:
        ret_type = self.scope.type_map.get('nil')

    if params is None:
        params = []

    if flags is None:
        flags = ir.FunctionFlags()

    def decorator(func):
        name = override_name or func.__name__
        if override_name is None:
            if name.startswith('_'):
                name = name[1:]

            if isinstance(self, (Class, GenericClass)):
                name = f'{self.type}.{name}'

        func.function = ir.Function(ir.Position.zero(), cast(ir.Type, ret_type), name, params, func, flags=flags)

        func.self = self
        if self is not None:
            self.attrs[name] = func.function
            info(f'Registered function \'{name}\' on {self.__class__.__name__}')

        return func

    return decorator

def overload(base, ret_type: Optional[ir.Type] = None, params: Optional[list[ir.Param]] = None):
    self = base.self

    if ret_type is None:
        ret_type = cast(ir.Type, self.scope.type_map.get('nil'))

    if params is None:
        params = []

    def decorator(func):
        name = func.__name__
        if name.startswith('_'):
            name = name[1:]

        if isinstance(self, Class):
            name = f'{self.type}.{name}'

        func.function = ir.Function(ir.Position.zero(), ret_type, name, params, func, flags=ir.FunctionFlags())

        func.self = self
        base.function.overloads.append(func.function)
        info(f'Added overload \'{name}\' to function \'{base.function.name}\'')
        return func

    return decorator


@dataclass
class DefinitionContext:
    pos: ir.Position
    scope: ir.Scope
    codegen: Any
    args: list[ir.Arg]
    
    def __post_init__(self):
        self.c_registry = cast(CRegistry, self.codegen.c_registry)
        self.builder = cast(lir.IRBuilder, self.codegen.builder)
        self.module = cast(lir.Module, self.codegen.module)
    
    @staticmethod
    def create(pos: ir.Position, scope: ir.Scope, codegen: Any, args: list[ir.Arg]):
        return DefinitionContext(pos, scope, codegen, args)
    
    def type(self, type: ir.Type):
        return self.codegen.visit_Type(type)
    
    def arg(self, index: int):
        return self.args[index]
    
    def arg_value(self, index: int):
        return self.arg(index).value
    
    def call(self, name: str, args: list[ir.Arg]):
        return self.codegen.visit_Call(ir.Call(self.pos, self.scope.type_map.get('any'), name, args))


class Lib:
    def __init__(self, scope: ir.Scope):
        self.attrs: dict[str, ir.Function] = {}
        self.scope = scope

        self.init()

    def init(self):
        pass
    
    def init_codegen(self, codegen):
        pass

    def add(self, lib: type[Union['Lib', 'Class']]):
        instance = lib(self.scope)
        self.attrs.update(instance.attrs)

    def add_to_scope(self):
        for k, v in self.attrs.items():
            self.scope.symbol_table.add(ir.Symbol(k, self.scope.type_map.get('function'), v))

class Class:
    def __init__(self, scope: ir.Scope):
        self.attrs: dict[str, ir.Function] = {}
        self.scope = scope

        self.name = self.__class__.__name__
        if not self.scope.type_map.has(self.name):
            self.scope.type_map.add(self.name)

        self.type = self.scope.type_map.get(self.name)
        self.init()

    def init(self):
        pass
    
    def init_codegen(self, codegen):
        pass

    def add_to_scope(self):
        for k, v in self.attrs.items():
            self.scope.symbol_table.add(ir.Symbol(k, self.scope.type_map.get('function'), v))

class GenericClass:
    def get_type_name(self):
        generics_str = ', '.join(str(g) for g in self.generics.values())
        return f'{self.base_name}<{generics_str}>'
    
    def __init__(self, scope: ir.Scope, **generics: ir.Type):
        self.attrs: dict[str, ir.Function] = {}
        self.generics = generics
        self.scope = scope
        
        self.base_name = self.__class__.__name__
        self.name = self.get_type_name()
        if not self.scope.type_map.has(self.name):
            self.scope.type_map.add(self.name)
        
        self.type = self.scope.type_map.get(self.name)
        self.init()
    
    def init(self):
        pass
    
    def init_codegen(self, codegen):
        pass
    
    def add_to_scope(self):
        for k, v in self.attrs.items():
            self.scope.symbol_table.add(ir.Symbol(k, self.scope.type_map.get('function'), v))
