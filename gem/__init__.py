from dataclasses import dataclass
from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path

from gem.passes.code_generation import CodeGenerationPass
from gem.passes.analyser import AnalyserPass
from gem.ir_builder import IRBuilder
from gem import ir


VERSION = '0.0.1'

@dataclass
class CompileOptions:
    clean: bool = False
    optimize: bool = False

def parse(scope: ir.Scope, _: CompileOptions):
    ir_builder = IRBuilder(scope)
    program = ir_builder.build()
    program.nodes.insert(0, ir.Use(program.pos, program.type, 'core'))
    return program

def compile_to_str(scope: ir.Scope, options: CompileOptions):
    program = parse(scope, options)
    info(f'Parsed Program:\n{program}')
    
    analysed_program = AnalyserPass.run(scope, options, program)
    info(f'Analysed Program:\n{analysed_program}')
    
    return CodeGenerationPass.run(scope, options, analysed_program)

def compile_to_ir(scope: ir.Scope, options: CompileOptions):
    code = compile_to_str(scope, options)
    ll_file = scope.file.with_suffix('.ll')
    ll_file.write_text(code)
    info(f'Wrote LLVM IR to {ll_file}')
    
    return ll_file
    
def compile_to_obj(scope: ir.Scope, options: CompileOptions):
    ll_file = compile_to_ir(scope, options)
    obj_file = scope.file.with_suffix('.o')
    optimize_flag = '-O3' if options.optimize else '-O0'
    cmd = f'clang -c -o {obj_file} {ll_file} -Wno-override-module -Wall -Werror -Wpedantic -Wextra {optimize_flag}'
    info(f'Executing compilation command: {cmd}')
    run(cmd, shell=True)
    info(f'Wrote object file to {obj_file}')
    
    if options.clean:
        ll_file.unlink()
    
    return obj_file

def compile_to_exe(scope: ir.Scope, options: CompileOptions):
    obj_file = compile_to_obj(scope, options)
    exe_file = scope.file.with_suffix('.exe')
    object_files_str = ' '.join(str(obj_file) for obj_file in scope.codegen_data.object_files)
    cmd = f'clang -o {exe_file} {obj_file} {object_files_str}'
    info(f'Executing compilation command: {cmd}')
    run(cmd, shell=True)
    info(f'Wrote executable to {exe_file}')
    
    if options.clean:
        obj_file.unlink()

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
    
    def option(self, name: str):
        for arg in self.args:
            if arg.startswith(f'--{name}'):
                return True
        
        return False
    
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
        options = CompileOptions(self.option('clean'))
        compile_to_exe(scope, options)
