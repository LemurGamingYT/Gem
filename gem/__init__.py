from ctypes import CFUNCTYPE, c_int
from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path

from llvmlite import binding as llvm

from gem.passes.code_generation import CodeGenerationPass
from gem.passes.analyser import AnalyserPass
from gem.ir_builder import IRBuilder
from gem import ir


VERSION = '0.0.1'

def parse(scope: ir.Scope):
    ir_builder = IRBuilder(scope)
    program = ir_builder.build()
    program.nodes.insert(0, ir.Use(program.pos, program.type, 'core'))
    return program

def compile_to_str(scope: ir.Scope):
    program = parse(scope)
    info(f'Parsed Program:\n{program}')
    
    analysed_program = AnalyserPass.run(scope, program)
    info(f'Analysed Program:\n{analysed_program}')
    
    return CodeGenerationPass.run(scope, analysed_program)

def compile_to_ir(scope: ir.Scope):
    code = compile_to_str(scope)
    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)
    info(f'Wrote LLVM IR to {ll_file}')
    
    return ll_file
    
def compile_to_obj(scope: ir.Scope):
    ll_file = compile_to_ir(scope)
    obj_file = scope.file.with_suffix('.o')
    extra_compilation_args_str = ' '.join(scope.extra_compilation_args)
    cmd = f'clang -c -o {obj_file} {ll_file} -Wno-override-module -Wall -Werror -Wpedantic -Wextra {extra_compilation_args_str}'
    info(f'Executing compilation command: {cmd}')
    run(cmd, shell=True)
    info(f'Wrote object file to {obj_file}')
    return obj_file

def compile_to_exe(scope: ir.Scope):
    obj_file = compile_to_obj(scope)
    exe_file = scope.file.with_suffix('.exe')
    extra_compilation_args_str = ' '.join(scope.extra_compilation_args)
    cmd = f'clang -o {exe_file} {obj_file} {extra_compilation_args_str}'
    info(f'Executing compilation command: {cmd}')
    run(cmd, shell=True)
    info(f'Wrote executable to {exe_file}')

def jit(scope: ir.Scope):
    ll_file = compile_to_ir(scope)
    code = ll_file.read_text('utf-8')
    target_machine = llvm.Target.from_default_triple().create_target_machine()
    backing_mod = llvm.parse_assembly('')
    with llvm.create_mcjit_compiler(backing_mod, target_machine) as engine:
        for arg in scope.extra_compilation_args:
            arg_path = Path(arg)
            if arg_path.is_file() and arg_path.suffix == '.ll':
                mod = llvm.parse_assembly(arg_path.read_text('utf-8'))
                engine.add_module(mod)
                
                info(f'Added module {arg_path}')
        
        mod = llvm.parse_assembly(code)
        engine.add_module(mod)
        engine.finalize_object()
        engine.run_static_constructors()
        
        info(f'Compiled module {ll_file}')
        
        main = CFUNCTYPE(c_int)(engine.get_function_address('main'))
        ret_code = main()
        print(f'main returned {ret_code}')

class ArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def get_actions(self):
        actions = []
        for key in dir(self):
            if key.startswith('action_'):
                actions.append(key.removeprefix('action_'))
        
        return actions
    
    def error(self, message: str):
        print(message)
        sys_exit(1)
    
    def parse(self):
        action = self.arg(0)
        if action is None:
            actions_str = '\n'.join(self.get_actions())
            self.error(f"""Usage: gem <action> ...options
Available actions:\n{actions_str}""")
        
        method = getattr(self, f'action_{action}', None)
        if method is None:
            self.error(f'unknown action \'{action}\'')
        
        return method()

    def arg(self, index: int):
        if index < len(self.args):
            return self.args[index]
        
        return None
    
    def action_run(self):
        file_path = self.arg(1)
        if file_path is None:
            print('Usage: gem build <file>')
            print('No file')
            sys_exit(1)
        
        path = Path(file_path)
        if not path.exists():
            print('Usage: gem build <file>')
            print(f'File \'{file_path}\' does not exist')
            sys_exit(1)
        
        if not path.is_file():
            print('Usage: gem build <file>')
            print(f'File \'{file_path}\' is not a file')
            sys_exit(1)
        
        scope = ir.Scope(path)
        jit(scope)
    
    def action_build(self):
        file_path = self.arg(1)
        if file_path is None:
            print('Usage: gem build <file>')
            print('No file')
            sys_exit(1)
        
        path = Path(file_path)
        if not path.exists():
            print('Usage: gem build <file>')
            print(f'File \'{file_path}\' does not exist')
            sys_exit(1)
        
        if not path.is_file():
            print('Usage: gem build <file>')
            print(f'File \'{file_path}\' is not a file')
            sys_exit(1)
        
        scope = ir.Scope(path)
        compile_to_exe(scope)
