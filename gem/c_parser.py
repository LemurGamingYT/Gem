from pathlib import Path
from typing import cast

from clang.cindex import Index, CursorKind, Cursor, Type as ClangType, Config, SourceLocation

from gem.ir import Scope, Function, Position, Body, Param, EnvItem, FunctionFlags


Config.set_library_path('C:/Program Files/LLVM/bin')

class GemCParser:
    def __init__(self, scope: Scope):
        self.scope = scope
    
    def parse_comment(self, comment: str | None) -> list[str]:
        if comment is None:
            return []
        
        if comment.startswith('/*'):
            comment = comment[2:-2]
        elif comment.startswith('//'):
            comment = comment[2:]
        
        return [flag[1:] for flag in comment.split() if flag.startswith('@')]
    
    def parse_type(self, cursor: ClangType):
        spelling = cursor.spelling
        is_reference = '*' in spelling
        if is_reference:
            spelling = spelling.replace(' *', '')
        
        type = self.scope.get_type(spelling)
        if spelling == 'void':
            type = self.scope.get_type('nil')

        if type is None:
            print(f'unknown type {spelling} (real type: \'{cursor.spelling}\')')
            return
        
        return type.as_reference() if is_reference else type

    def parse_function(self, node: Cursor):
        comment_flags = self.parse_comment(node.raw_comment)
        if 'public' not in comment_flags:
            return

        location = cast(SourceLocation, node.location)
        ret_type = self.parse_type(node.result_type)
        if ret_type is None:
            return
        
        params = []
        for param in node.get_arguments():
            ploc = cast(SourceLocation, param.location)
            param_type = self.parse_type(param.type)
            if param_type is None:
                return
            
            params.append(Param(Position(ploc.line, ploc.column), param_type, node.spelling))
        
        pos = Position(location.line, location.column)
        flags = FunctionFlags()
        for flag in comment_flags:
            setattr(flags, flag, True)
        
        func = Function(
            pos, ret_type, node.spelling, params,
            Body(pos, self.scope.get_type('nil')),
            flags=flags
        )
        for flag in comment_flags:
            if flag.startswith('overload('):
                func_name = flag.removeprefix('overload(').removesuffix(')')
                f = self.scope.get_env(func_name)
                if f is None or f.value is None:
                    print(f'unknown function {func_name}')
                    return
                
                f.value.overloads.append(func)
                return
        
        self.scope.set_env(EnvItem(node.spelling, self.scope.get_type('function'), func))

    def parse_file(self, header: Path):
        index = Index.create()
        tu = index.parse(str(header), args=['-fparse-all-comments', '-fsyntax-only'])
        for cursor in tu.cursor.walk_preorder():
            if cursor.kind == CursorKind.FUNCTION_DECL:
                self.parse_function(cursor)
