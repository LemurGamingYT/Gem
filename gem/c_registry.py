from dataclasses import dataclass
from typing import Optional, cast
from logging import info

from llvmlite import ir as lir

from gem import ir


class UnknownCObject(Exception):
    pass

@dataclass
class CFunction:
    func_type: lir.FunctionType
    llvm_name: Optional[str] = None

@dataclass
class CGlobal:
    type: lir.Type
    initializer: Optional[lir.Constant] = None
    llvm_name: Optional[str] = None

class CRegistry:
    @staticmethod
    def get_all_cobjects():
        FILE_type = lir.LiteralStructType([lir.PointerType(lir.IntType(8))])
        return {
            'malloc': CFunction(lir.FunctionType(lir.PointerType(lir.IntType(8)), [
                lir.IntType(32)
            ])),
            'calloc': CFunction(lir.FunctionType(lir.PointerType(lir.IntType(8)), [
                lir.IntType(32),
                lir.IntType(32)
            ])),
            'realloc': CFunction(lir.FunctionType(lir.PointerType(lir.IntType(8)), [
                lir.PointerType(lir.IntType(8)),
                lir.IntType(32)
            ])),
            'free': CFunction(lir.FunctionType(lir.VoidType(), [
                lir.PointerType(lir.IntType(8))
            ])),
            'memcpy': CFunction(lir.FunctionType(lir.VoidType(), [
                lir.PointerType(lir.IntType(8)),
                lir.PointerType(lir.IntType(8)),
                lir.IntType(32),
                lir.IntType(1)
            ]), 'llvm.memcpy.p0.p0.i32'),
            'puts': CFunction(lir.FunctionType(lir.VoidType(), [
                lir.PointerType(lir.IntType(8))
            ])),
            'exit': CFunction(lir.FunctionType(lir.VoidType(), [
                lir.IntType(32)
            ])),
            'snprintf': CFunction(lir.FunctionType(lir.IntType(32), [
                lir.PointerType(lir.IntType(8)),
                lir.IntType(32),
                lir.PointerType(lir.IntType(8))
            ], True)),
            'asprintf': CFunction(lir.FunctionType(lir.IntType(32), [
                lir.PointerType(lir.PointerType(lir.IntType(8))),
                lir.PointerType(lir.IntType(8))
            ], True)),
            'fgets': CFunction(lir.FunctionType(lir.VoidType(), [
                lir.PointerType(lir.IntType(8)),
                lir.IntType(32),
                FILE_type
            ])),
            '__acrt_iob_func': CFunction(lir.FunctionType(FILE_type, [lir.IntType(32)])),
            'strlen': CFunction(lir.FunctionType(lir.IntType(32), [lir.PointerType(lir.IntType(8))])),
            'printf': CFunction(lir.FunctionType(lir.VoidType(), [lir.PointerType(lir.IntType(8))], True))
        }
    
    def __init__(self, module: lir.Module, file: ir.File):
        self.module = module
        self.file = file

        self.c_globals: dict[str, CGlobal] = {}
        self.c_funcs: dict[str, CFunction] = {}
        
        for name, cobj in self.get_all_cobjects().items():
            self.register(name, cobj)

    def register(self, name: str, cobj: CFunction | CGlobal):
        if isinstance(cobj, CFunction):
            info(f'Registered C function \'{name}\'')
            self.c_funcs[name] = cobj
        elif isinstance(cobj, CGlobal):
            info(f'Registered C global \'{name}\'')
            self.c_globals[name] = cobj
    
    def _lookup_function(self, name: str):
        cfunc = self.c_funcs.get(name)
        if cfunc is None:
            raise UnknownCObject(f'Unknown C function \'{name}\'')
        
        llvm_name = cfunc.llvm_name or name
        if llvm_name in self.module.globals:
            return self.module.get_global(llvm_name)

        func = lir.Function(self.module, cfunc.func_type, llvm_name)
        func.linkage = 'external'

        return func
    
    def _lookup_global(self, name: str):
        cglobal = self.c_globals.get(name)
        if cglobal is None:
            raise UnknownCObject(f'Unknown C global \'{name}\'')

        llvm_name = cglobal.llvm_name or name
        if llvm_name in self.module.globals:
            return self.module.get_global(llvm_name)

        global_var = lir.GlobalVariable(self.module, cglobal.type, llvm_name)
        global_var.linkage = 'external'
        
        if cglobal.initializer is not None:
            global_var.initializer = cast(None, cglobal.initializer)
        
        return global_var
    
    def get(self, name: str) -> lir.Function | lir.GlobalVariable:
        if name in self.c_funcs:
            return self._lookup_function(name)
        elif name in self.c_globals:
            return self._lookup_global(name)
        
        raise ValueError(f'Unknown C object \'{name}\'')
