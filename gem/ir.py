from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from sys import exit as sys_exit
from typing import Optional, Any
from logging import error, info
from pathlib import Path
from copy import copy

from colorama import Fore, Style


STDLIB_PATH = Path(__file__).parent / 'stdlib'

@dataclass(unsafe_hash=True)
class Position:
    line: int
    column: int
    
    @staticmethod
    def zero():
        return Position(0, 0)

    def comptime_error(self, file: 'File', message: str):
        src = file.path.read_text('utf-8')
        print(src.splitlines()[self.line - 1])
        print(' ' * self.column + '^')
        print(f'{Style.BRIGHT}{Fore.RED}error: {message}{Style.RESET_ALL}')
        error(message)
        
        if file.options.debug:
            raise NotImplementedError(message)
        
        sys_exit(1)

@dataclass
class Symbol:
    name: str
    type: 'Type'
    value: Any
    is_mutable: bool = False

@dataclass
class SymbolTable:
    symbols: dict[str, Symbol] = field(default_factory=dict)

    def get(self, name: str):
        return self.symbols.get(name)
                 
    def add(self, symbol: Symbol):
        self.symbols[symbol.name] = symbol
    
    def has(self, name: str):
        return name in self.symbols
                 
    def remove(self, name: str):
        if self.has(name):
            del self.symbols[name]
    
    def clone(self):
        return SymbolTable(self.symbols.copy())
    
    def merge(self, other: 'SymbolTable'):
        self.symbols.update(other.symbols)
                 
@dataclass
class TypeMap:
    types: dict[str, 'Type'] = field(default_factory=dict)
                 
    def tryget(self, name: str):
        return self.types.get(name)
    
    def get(self, name: str):
        return self.types[name]
                 
    def add(self, display: str, typ: str | None = None):
        self.types[display] = Type(Position.zero(), typ or display, display)
    
    def add_type(self, display: str, typ: 'Type'):
        self.types[display] = typ
    
    def has(self, name: str):
        return name in self.types
                 
    def remove(self, name: str):
        if self.has(name):
            del self.types[name]
    
    def clone(self):
        return TypeMap(self.types.copy())
    
    def merge(self, other: 'TypeMap'):
        self.types.update(other.types)

@dataclass
class CodegenData:
    object_files: list[Path] = field(default_factory=list)

@dataclass
class Scope:
    parent: Optional['Scope'] = None
    symbol_table: SymbolTable = field(default_factory=SymbolTable)
    type_map: TypeMap = field(default_factory=TypeMap)
    dependencies: list[Path] = field(default_factory=list)
    
    @property
    def unique_name(self):
        return f'_{self._unique_name_idx}'

    def __post_init__(self):
        if self.parent is not None:
            self._unique_name_idx = self.parent._unique_name_idx + 1

            self.symbol_table = self.parent.symbol_table.clone()
            self.type_map = self.parent.type_map.clone()
            
            self.dependencies = self.parent.dependencies
        else:
            self._unique_name_idx = 0
            
            self.type_map.add('int')
            self.type_map.add('float')
            self.type_map.add('string')
            self.type_map.add('bool')
            self.type_map.add('nil')
            
            self.type_map.add('any')
            self.type_map.add('pointer')
            self.type_map.add('function')
    
    def merge(self, other: 'Scope'):
        self.symbol_table.merge(other.symbol_table)
        self.type_map.merge(other.type_map)

    def make_child(self) -> 'Scope':
        return Scope(self)

@dataclass
class CompileOptions:
    clean: bool = False
    optimize: bool = False
    debug: bool = False

@dataclass
class File:
    path: Path
    scope: Scope
    options: CompileOptions
    program: Optional['Program'] = None
    codegen_data: CodegenData = field(default_factory=CodegenData)


@dataclass(unsafe_hash=True)
class Node(ABC):
    pos: Position
    type: 'Type'
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    def to_arg(self) -> 'Arg':
        return Arg(self.pos, self.type, self)
    
    def clone(self) -> 'Node':
        return copy(self)

@dataclass(unsafe_hash=True)
class Type(Node):
    type: str #type: ignore
    display: str
    
    @staticmethod
    def new(type: str, display: Optional[str] = None) -> 'Type':
        return Type(Position.zero(), type, display or type)
    
    def __str__(self) -> str:
        return self.display

@dataclass
class Program(Node):
    nodes: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        return '\n'.join(str(node) for node in self.nodes)

@dataclass
class Param(Node):
    name: str
    is_mutable: bool = False
    
    def __str__(self) -> str:
        return f'{self.type} {self.name}'

@dataclass
class Arg(Node):
    value: Any
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class Body(Node):
    nodes: list[Node] = field(default_factory=list)
    
    def __str__(self) -> str:
        return '\n'.join(str(node) for node in self.nodes)

@dataclass(kw_only=True)
class FunctionFlags:
    static: bool = False
    property: bool = False
    method: bool = False
    extern: bool = False
    
    def __str__(self) -> str:
        flags = ''
        if self.static:
            flags += 'static '
        
        if self.property:
            flags += 'property '
        
        if self.method:
            flags += 'method '
        
        if self.extern:
            flags += 'extern '
        
        return flags

@dataclass
class Function(Node):
    name: str
    params: list[Param] = field(default_factory=list)
    body: Body | None = field(default=None)
    overloads: list['Function'] = field(default_factory=list)
    flags: FunctionFlags = field(default_factory=FunctionFlags)
    extend_type: Type | None = None
    generic_params: list[str] = field(default_factory=list)
    
    @property
    def ret_type(self):
        return self.type
    
    @property
    def is_generic(self):
        return len(self.generic_params) > 0
    
    def match_params(self, args: list[Arg]):
        if len(args) != len(self.params):
            info(f'Number of arguments ({len(args)}) does not match the number of parameters ({len(self.params)})')
            return False
        
        for arg, param in zip(args, self.params):
            param_type = param.type
            arg_type = arg.type
            if str(arg_type) != str(param_type) and param_type.type != 'any' and param_type.type not in self.generic_params:
                info(f'Type mismatch: arg type {arg_type} does not match param type {param_type}')
                return False
        
        return True
    
    def __str__(self) -> str:
        params_str = ', '.join(str(param) for param in self.params)
        extend_str = f'{self.extend_type}.' if self.extend_type else ''
        generics_str = ('<' + ', '.join(self.generic_params) + '>') if len(self.generic_params) > 0 else ''
        signature = f'{self.flags}fn {extend_str}{self.name}{generics_str}({params_str}) -> {self.ret_type}'
        if self.body is None:
            return signature
        
        return f"""{signature} {{
{self.body}
}}"""

    def call(self, pos: Position, args: list[Arg]):
        return Call(pos, self.ret_type, self.name, args)
    
    def create_generic_map(self, args: list[Arg]):
        generic_map = {}
        for param, arg in zip(self.params, args):
            if str(param.type) not in self.generic_params:
                continue
            
            generic_map[str(param.type)] = arg.type
        
        return generic_map

@dataclass
class Variable(Node):
    name: str
    value: Node
    is_mutable: bool = False
    op: str | None = None
    
    def __str__(self) -> str:
        return f'{"mut" if self.is_mutable else ""}{self.type} {self.name} = {self.value}'

@dataclass
class Assignment(Node):
    name: str
    value: Node
    op: str | None = None
    
    def __str__(self) -> str:
        return f'{self.name} {self.op if self.op is not None else ""}= {self.value}'

@dataclass
class Elseif(Node):
    cond: Node
    body: Body
    
    def __str__(self) -> str:
        return f"""else if {self.cond} {{
{self.body}
}}"""

@dataclass
class If(Node):
    cond: Node
    body: Body
    else_body: Body | None = field(default=None)
    elseifs: list[Elseif] = field(default_factory=list)
    
    def __str__(self) -> str:
        elseifs_str = ''.join(str(elseif) for elseif in self.elseifs)
        return f"""if {self.cond} {{
{self.body}
}}{elseifs_str}{self.else_body if self.else_body is not None else ''}"""

@dataclass
class While(Node):
    cond: Node
    body: Body
    
    def __str__(self) -> str:
        return f"""while {self.cond} {{
{self.body}
}}"""

@dataclass
class Break(Node):
    def __str__(self) -> str:
        return 'break'

@dataclass
class Continue(Node):
    def __str__(self) -> str:
        return 'continue'

@dataclass
class Use(Node):
    path: str
    
    def __str__(self) -> str:
        return f'use "{self.path}"'

@dataclass
class Return(Node):
    value: Node
    
    def __str__(self) -> str:
        return f'return {self.value}'

@dataclass
class Int(Node):
    value: int
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class Float(Node):
    value: float
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class String(Node):
    value: str
    
    def __str__(self) -> str:
        return f'"{self.value}"'

@dataclass
class StringLiteral(Node):
    value: str
    
    def __str__(self) -> str:
        return f'str_lit("{self.value}")'

@dataclass
class Bool(Node):
    value: bool
    
    def __str__(self) -> str:
        return f'{self.value}'

@dataclass
class Id(Node):
    name: str
    
    def __str__(self) -> str:
        return self.name

@dataclass
class Ternary(Node):
    cond: Node
    true: Node
    false: Node
    
    def __str__(self) -> str:
        return f'{self.true} if {self.cond} else {self.false}'

@dataclass
class Bracketed(Node):
    value: Node
    
    def __str__(self) -> str:
        return f'({self.value})'

@dataclass
class Call(Node):
    callee: str
    args: list[Arg] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(str(arg) for arg in self.args)
        return f'{self.callee}({args_str})'

@dataclass
class Cast(Node):
    value: Node
    
    def __str__(self) -> str:
        return f'({self.value})'

@dataclass
class New(Node):
    new_type: Type
    args: list[Arg] = field(default_factory=list)
    
    def __str__(self) -> str:
        args_str = ', '.join(str(arg) for arg in self.args)
        return f'new {self.new_type}({args_str})'

@dataclass
class Operation(Node):
    op: str
    left: Node
    right: Node
    
    def __str__(self) -> str:
        return f'{self.left} {self.op} {self.right}'

@dataclass
class UnaryOperation(Node):
    op: str
    value: Node
    
    def __str__(self) -> str:
        return f'{self.op}{self.value}'

@dataclass
class Attribute(Node):
    value: Node
    attr: str
    args: list[Arg] | None = None
    
    def __str__(self) -> str:
        if self.args is None:
            return f'{self.value}.{self.attr}'
        
        args_str = ', '.join(str(arg) for arg in self.args)
        return f'{self.value}.{self.attr}({args_str})'
