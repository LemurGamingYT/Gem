from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path

from gem.passes.code_generation import CodeGenerationPass
from gem.passes.memory_manager import MemoryManager
from gem.passes.analyser import AnalyserPass
from gem.ir_builder import IRBuilder
from gem import ir


VERSION = '0.0.1'
CRUNTIME_DIR = Path(__file__).parent / 'cruntime'

def parse(file: ir.File):
    ir_builder = IRBuilder(file)
    program = ir_builder.build()
    program.nodes.insert(0, ir.Use(program.pos, 'core'))
    return program

def compile_to_str(file: ir.File):
    program = parse(file)
    ir_file = file.path.with_suffix('.gir')
    if file.options.debug:
        ir_file.write_text(str(program))
    
    analysed_program = AnalyserPass.run(file, program)
    if file.options.debug:
        ir_file.write_text(str(analysed_program))
    
    memory_safe_program = MemoryManager.run(file, analysed_program)
    if file.options.debug:
        ir_file.write_text(str(memory_safe_program))
    
    return CodeGenerationPass.run(file, memory_safe_program)

def compile_to_ir(file: ir.File):
    code = compile_to_str(file)
    ll_file = file.path.with_suffix('.ll')
    ll_file.write_text(code)
    return ll_file
    
def compile_to_obj(file: ir.File):
    ll_file = compile_to_ir(file)
    obj_file = file.path.with_suffix('.o')
    flags = ['-Wno-override-module', '-Wall', '-Werror', '-Wpedantic', '-Wextra']
    if file.options.optimize:
        flags.append('-O2')
    
    flags_str = ' '.join(flags)
    cmd = f'clang -c -o {obj_file} {ll_file} {flags_str}'
    info(f'Executing compilation command: {cmd}')
    run(cmd, shell=True)
    info(f'Wrote object file to {obj_file}')
    
    if file.options.clean:
        ll_file.unlink()
    
    return obj_file

def compile_to_exe(file: ir.File):
    obj_file = compile_to_obj(file)
    exe_file = file.path.with_suffix('.exe')
    object_files = file.codegen_data.object_files
    object_files.append(obj_file)
    for cfile in CRUNTIME_DIR.rglob('*.c'):
        cobj = cfile.with_suffix('.o')
        cmd = f'clang -c -o {cobj} {cfile}'
        info(f'Executing compilation command: {cmd}')
        
        run(cmd, shell=True)
        object_files.append(cobj)
    
    object_files_str = ' '.join(str(obj_file) for obj_file in object_files)
    cmd = f'clang -o {exe_file} {object_files_str}'
    info(f'Executing compilation command: {cmd}')
    run(cmd, shell=True)
    info(f'Wrote executable to {exe_file}')
    
    if file.options.clean:
        for obj in object_files:
            obj.unlink()

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
        
        options = ir.CompileOptions(self.option('clean'), self.option('optimize'), self.option('debug'))
        file = ir.File(path, ir.Scope(), options)
        compile_to_exe(file)
