from typing import Any, Union, Callable, TypeVar
from dataclasses import dataclass, field
from importlib import import_module
from sys import exit as sys_exit
from pathlib import Path

from colorama import Fore, Style


T = TypeVar('T')
stdlib_path = (Path(__file__).parent / 'stdlib').absolute()


def function(pos: 'Position', scope: 'Scope', params: list[tuple[str, 'Type']], ret_type: 'Type'):
    def decorator(func: Callable[['CallContext'], 'Node']):
        name = func.__name__[1:] if func.__name__.startswith('_') else func.__name__
        f = Function(
            pos, ret_type, name, [Param(pos, type, name) for name, type in params],
            callable=func
        )

        setattr(func, '__function__', f)
        scope.set_env(EnvItem(name, scope.get_type('function'), f))
        return func
    
    return decorator

def get_end_points(nodes: list['Node']):
    end_points: list[tuple[int, Node]] = []
    for i, node in enumerate(nodes):
        if isinstance(node, Return):
            end_points.append((i, node))
        elif isinstance(node, Body):
            end_points.extend(get_end_points(node.body))
    
    return end_points

@dataclass
class Position:
    line: int
    column: int

    def comptime_error(self, scope, message: str):
        src = scope.src
        print(src.splitlines()[self.line - 1])
        print(' ' * self.column + '^')
        print(f'{Fore.RED}{Style.BRIGHT}error: {message}{Style.RESET_ALL}')
        sys_exit(1)


@dataclass
class Type:
    display: str
    c_type: str
    is_reference: bool = False

    def __str__(self):
        return self.display
    
    def __repr__(self):
        return self.__str__()
    
    def as_reference(self):
        return Type(self.display, self.c_type, True)


@dataclass
class EnvItem:
    name: str
    type: Type
    value: Any
    is_const: bool = False

    def free_method(self, scope: 'Scope'):
        return scope.get_env(f'free_{self.type}')

@dataclass
class Scope:
    file: Path
    pos: Position
    parent: Union['Scope', None] = None
    env: dict[str, EnvItem] = field(default_factory=dict)
    types: dict[str, Type] = field(default_factory=dict)
    includes: list[str] = field(default_factory=list)
    toplevel_code: list[str] = field(default_factory=list)
    compile_args: list[str] = field(default_factory=list)
    is_loop: bool = False
    
    @staticmethod
    def make_global(file: Path, pos: Position):
        return Scope(file, pos)
    
    @property
    def includes_str(self):
        return '\n'.join(f'#include "{include}"' for include in self.includes)
    
    @property
    def toplevel_str(self):
        return '\n'.join(self.toplevel_code)
    
    @property
    def unique_name(self):
        self._unique_name_idx += 1
        return f'_{self._unique_name_idx}'

    def __post_init__(self):
        self.src = self.file.read_text()
        if self.parent is not None:
            self.env = self.parent.env.copy()
            self.types = self.parent.types.copy()
            self.compile_args = self.parent.compile_args
            self.toplevel_code = self.parent.toplevel_code
            self.includes = self.parent.includes
            self._unique_name_idx = self.parent._unique_name_idx + 1
        else:
            self._add_default_types()

            self.use('builtins', Position(1, 0))

            self._unique_name_idx = 0
    
    def _add_default_types(self):
        self.set_type(Type('int', 'int'))
        self.set_type(Type('float', 'float'))
        self.set_type(Type('bool', 'bool'))
        self.set_type(Type('string', 'string'))
        self.set_type(Type('nil', 'nil'))
        self.set_type(Type('array', 'array'))
        self.set_type(Type('function', 'function'))

        self.set_type(Type('Ref', 'Ref'))
        self.set_type(Type('Math', 'Math'))
        
        self.set_type(Type('string_lit', 'string_lit'))
        self.set_type(Type('function', 'function'))
        self.set_type(Type('any', 'any'))
    
    def include(self, path: str):
        if path in self.includes:
            return
        
        self.includes.append(path)
    
    def add_toplevel_code(self, code: str):
        self.toplevel_code.append(code)
    
    def make_child(self, pos: Position):
        return Scope(self.file, pos, self)
    
    def use(self, name: str, pos: Position):
        path = stdlib_path / name
        if not path.exists():
            pos.comptime_error(self, f'unknown library name \'{name}\'')
        
        from gem.c_parser import GemCParser

        c_parser = GemCParser(self)
        for header in path.glob('*.h'):
            c_parser.parse_file(header)
            self.include(header.absolute().as_posix())
        
        for c_file in path.glob('*.c'):
            self.compile_args.append(c_file.absolute().as_posix())
        
        has_python = (path / '__init__.py').is_file()
        if has_python:
            module = import_module(f'gem.stdlib.{name}')
            module.setup(self, pos)
    
    def get_env(self, name: str):
        item = self.env.get(name)
        if item is not None:
            return item

        if self.parent is not None:
            return self.parent.get_env(name)

        return None
    
    def set_env(self, item: EnvItem, name: str | None = None):
        if name is None:
            name = item.name
        
        self.env[name] = item
        if self.parent is not None:
            self.parent.set_env(item, name)
    
    def get_type(self, name: str) -> Any: # use an Any type so the caller don't need to cast it
        type = self.types.get(name)
        if type is not None:
            return type
        
        if self.parent is not None:
            return self.parent.get_type(name)
    
        return None
    
    def set_type(self, type: Type, name: str | None = None):
        if name is None:
            name = type.display

        self.types[name] = type
        if self.parent is not None:
            self.parent.set_type(type, name)
    
    def remove_env(self, name: str):
        if self.parent is not None:
            self.parent.remove_env(name)

        if name in self.env:
            del self.env[name]
    
    def remove_type(self, name: str):
        if self.parent is not None:
            self.parent.remove_type(name)
        
        if name in self.types:
            del self.types[name]

@dataclass
class CallContext:
    scope: Scope
    pos: Position
    func: 'Function'
    args: list['Node']

    @staticmethod
    def from_name(pos: Position, scope: Scope, name: str, args: list['Node']):
        item = scope.get_env(name)
        if item is None:
            return None
        
        func = item.value
        if not isinstance(func, Function):
            return None
        
        return CallContext(scope, pos, func, args)

    def __post_init__(self):
        self.params = self.func.params
        self.ret_type = self.func.type

        self._param_arg_map = {}
    
    def _invoke_function(self, func: 'Function'):
        if len(self.args) != len(func.params):
            return False
        
        for param, arg in zip(func.params, self.args):
            if param.type != arg.type and str(param.type) != 'any':
                return False
        
        return True
    
    def invoke(self):
        func = self.func
        if not self._invoke_function(func):
            for overload in func.overloads:
                if self._invoke_function(overload):
                    func = overload
                    break
            else:
                arg_types = ', '.join(str(arg.type) for arg in self.args)
                self.pos.comptime_error(
                    self.scope,
                    f'no matching overload for function \'{func.name}\' with types {arg_types}'
                )
        
        for param, arg in zip(func.params, self.args):
            self._param_arg_map[param.name] = arg
        
        if func.callable is not None:
            return func.callable(self)

        return Call(self.pos, func.type, func.name, self.args)
    
    def call(self, name: str, args: list['Node']):
        ctx = CallContext.from_name(self.pos, self.scope, name, args)
        if ctx is None:
            self.pos.comptime_error(self.scope, f'unknown callable \'{name}\'')
        
        return ctx.invoke()
    
    def get_arg(self, name: str) -> 'Node':
        arg = self._param_arg_map.get(name)
        if arg is None:
            self.scope.pos.comptime_error(self.scope, f'argument \'{name}\' not found')
        
        return arg


@dataclass
class Node:
    pos: Position
    type: Type
    parent: Union['Node', None] = field(kw_only=True, default=None, repr=False)

    def apply_self_as_parent(self, x: Union[None, list, tuple, dict, 'Node']):
        if x is None:
            return

        if isinstance(x, (list, tuple)):
            for n in x:
                self.apply_self_as_parent(n)
        elif isinstance(x, dict):
            for k, v in x.items():
                self.apply_self_as_parent(k)
                self.apply_self_as_parent(v)
        elif isinstance(x, Node):
            x.parent = self
    
    def has_parent(self, of_type: T) -> Union[T, None]:
        if isinstance(self.parent, of_type): # type: ignore
            return self.parent # type: ignore
        
        if self.parent is None:
            return None
        
        return self.parent.has_parent(of_type)
    
    def get_children(self) -> list['Node']:
        children = []
        for k, v in self.__dict__.items():
            if k == 'parent':
                continue

            if isinstance(v, Node):
                children.append(v)
            elif isinstance(v, (list, tuple)):
                for n in v:
                    children.append(n)
        
        return children
    
    def get_child(self, of_type: T) -> T | None:
        for child in self.get_children():
            if isinstance(child, of_type): # type: ignore
                return child # type: ignore
        
        return None
    
    def get_descendants(self) -> list['Node']:
        descendants = []
        for child in self.get_children():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        
        return descendants

@dataclass
class Program(Node):
    stmts: list[Node] = field(default_factory=list)

    def __post_init__(self):
        self.apply_self_as_parent(self.stmts)

@dataclass
class Param(Node):
    name: str
    type: Type

@dataclass
class Body(Node):
    body: list[Node] = field(default_factory=list)

    def __post_init__(self):
        self.apply_self_as_parent(self.body)

@dataclass(kw_only=True)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False

@dataclass
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    body: Body | None = None
    callable: Callable[[CallContext], Node] | None = None
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    generic_names: list[str] | None = None

    @property
    def is_declaration(self):
        return self.body is None
    
    def __post_init__(self):
        self.generic_types = []
        self.overloads = []

        self.apply_self_as_parent(self.params)
        self.apply_self_as_parent(self.body)

@dataclass
class Variable(Node):
    name: str
    type: Type
    value: Node
    is_assignment: bool = False
    is_const: bool = False
    op: str | None = None

    def __post_init__(self):
        self.apply_self_as_parent(self.value)

@dataclass
class Return(Node):
    value: Node

    def __post_init__(self):
        self.apply_self_as_parent(self.value)

@dataclass
class Constant(Node):
    value: Any

@dataclass
class Call(Node):
    name: str
    args: list[Node] = field(default_factory=list)

    def __post_init__(self):
        self.apply_self_as_parent(self.args)

@dataclass
class Id(Node):
    name: str

@dataclass
class Bracketed(Node):
    value: Node

    def __post_init__(self):
        self.apply_self_as_parent(self.value)

@dataclass
class Attribute(Node):
    value: Node
    attr: str
    args: list[Node] | None = None
    object_is_a_pointer: bool = False

    def __post_init__(self):
        self.apply_self_as_parent(self.value)
        self.apply_self_as_parent(self.args)

@dataclass
class Operation(Node):
    op: str
    lhs: Node
    rhs: Node

    def __post_init__(self):
        self.apply_self_as_parent(self.lhs)
        self.apply_self_as_parent(self.rhs)

@dataclass
class Cast(Node):
    value: Node

    def __post_init__(self):
        self.apply_self_as_parent(self.value)

@dataclass
class Reference(Node):
    name: Id

    def __post_init__(self):
        self.apply_self_as_parent(self.name)

@dataclass
class If(Node):
    cond: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[tuple[Node, Body]] = field(default_factory=list)

    def __post_init__(self):
        self.apply_self_as_parent(self.cond)
        self.apply_self_as_parent(self.body)
        self.apply_self_as_parent(self.else_body)
        self.apply_self_as_parent(self.elseifs)

@dataclass
class While(Node):
    cond: Node
    body: Body

    def __post_init__(self):
        self.apply_self_as_parent(self.cond)
        self.apply_self_as_parent(self.body)

@dataclass
class Break(Node):
    pass

@dataclass
class Continue(Node):
    pass

@dataclass
class Ternary(Node):
    cond: Node
    true: Node
    false: Node

    def __post_init__(self):
        self.apply_self_as_parent(self.cond)
        self.apply_self_as_parent(self.true)
        self.apply_self_as_parent(self.false)

@dataclass
class Foreach(Node):
    var_name: str
    iterable: Node
    body: Body
    
    def __post_init__(self):
        self.apply_self_as_parent(self.iterable)
        self.apply_self_as_parent(self.body)

@dataclass
class For(Node):
    var_name: str
    start: Node
    end: Node
    step: Node
    body: Body

    def __post_init__(self):
        self.apply_self_as_parent(self.start)
        self.apply_self_as_parent(self.end)
        self.apply_self_as_parent(self.step)
        self.apply_self_as_parent(self.body)

@dataclass
class Increment(Node):
    var: Id

@dataclass
class Decrement(Node):
    var: Id
