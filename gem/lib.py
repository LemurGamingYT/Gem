from typing import Optional, cast, Union, Any
from dataclasses import dataclass
from logging import info

from llvmlite import ir as lir

from gem.codegen_utils import create_string_constant, llint
from gem.c_registry import CRegistry
from gem import ir


class UnknownFunctionError(Exception):
    pass

class InvalidArgumentError(Exception):
    pass


def builtin(self, ret_type: Optional[ir.Type] = None, params: Optional[list[ir.Param]] = None,
            flags: Optional[ir.FunctionFlags] = None, override_name: Optional[str] = None):
    if ret_type is None:
        ret_type = cast(ir.Type, self.scope.type_map.get('nil'))

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

        func.function = ir.Function(ir.Position.zero(), ret_type, name, params, func, flags=flags)

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
class LoadedArg:
    pos: ir.Position
    type: ir.Type
    param_name: str
    value: Any

@dataclass
class DefinitionContext:
    file: ir.File
    func: ir.Function
    codegen: Any
    callsite: Optional[ir.Call] = None

    def __post_init__(self):
        self.pos = self.callsite.pos if self.callsite is not None else self.func.pos
        self.args = self.callsite.args if self.callsite is not None else []
        
        self.scope = self.file.scope

        self.ret_type = self.func.ret_type
        self.params = self.func.params

        self.builder = cast(lir.IRBuilder, self.codegen.builder)
        self.module = cast(lir.Module, self.codegen.module)

        self.c_registry = cast(CRegistry, getattr(self.module, 'c_registry'))

    @staticmethod
    def create(file: ir.File, codegen, name: str, callsite: Optional[ir.Call] = None):
        symbol = file.scope.symbol_table.get(name)
        if symbol is None:
            return

        return DefinitionContext(file, symbol.value, codegen, callsite)

    def type(self, type: ir.Type) -> lir.Type:
        return self.codegen.visit(type)

    def arg(self, index: int):
        param = self.params[index]
        symbol = self.scope.symbol_table.get(param.name)
        if symbol is None:
            raise InvalidArgumentError(f'unknown argument \'{param.name}\'')

        arg_type = symbol.type
        if self.args:
            arg_type = self.args[index].type

        return LoadedArg(param.pos, arg_type, param.name, symbol.value)

    def arg_type(self, index: int):
        return self.arg(index).type

    def arg_value(self, index: int) -> lir.LoadInstr:
        arg = self.arg(index)
        return self.builder.load(arg.value, arg.param_name)
    
    def arg_ptr(self, index: int) -> lir.LoadInstr:
        return self.arg(index).value

    def arg_type_and_value(self, index: int):
        arg = self.arg(index)
        return arg.type, self.builder.load(arg.value, arg.param_name)

    def call(self, name: str, args: list[ir.Arg]):
        return self.codegen.call_func(self.pos, name, args)

    def error(self, message: str):
        self.call('error', [ir.Arg(self.pos, self.scope.type_map.get('pointer'), create_string_constant(
            self.module, message
        ))])
    
    def string_lit(self, s: str):
        return self.call('string.new', [
            ir.Arg(self.pos, self.scope.type_map.get('pointer'), create_string_constant(self.module, s)),
            ir.Arg(self.pos, self.scope.type_map.get('int'), llint(len(s)))
        ])


class Lib:
    def __init__(self, file: ir.File):
        self.attrs: dict[str, ir.Function] = {}
        self.file = file
        self.scope = self.file.scope

        self.init()

    def init(self):
        pass
    
    def init_codegen(self, codegen):
        pass

    def add(self, lib: type[Union['Lib', 'Class']]):
        instance = lib(self.file)
        self.attrs.update(instance.attrs)

    def add_to_scope(self):
        for k, v in self.attrs.items():
            self.scope.symbol_table.add(ir.Symbol(k, self.scope.type_map.get('function'), v, self.file))

class Class:
    def __init__(self, file: ir.File):
        self.attrs: dict[str, ir.Function] = {}
        self.file = file
        self.scope = self.file.scope

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
    
    def __init__(self, file: ir.File, **generics: ir.Type):
        self.attrs: dict[str, ir.Function] = {}
        self.generics = generics
        self.file = file
        self.scope = self.file.scope
        
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
