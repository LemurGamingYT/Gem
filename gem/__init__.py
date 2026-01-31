from sys import exit as sys_exit
from subprocess import run
from logging import info
from pathlib import Path

from gem.passes.name_type_resolver import NameAndTypeResolverPass
from gem.passes.code_generation import CodeGenerationPass
from gem.passes.memory_manager import MemoryManagerPass
from gem.passes.node_expansion import NodeExpansionPass
from gem.ir_builder import IRBuilder
from gem import ir


VERSION = '0.0.1'
GEM_DIR = Path(__file__).parent
CRUNTIME_DIR = GEM_DIR / 'cruntime'
TESTS_DIR = GEM_DIR / 'tests'

PASSES = [NameAndTypeResolverPass, NodeExpansionPass, MemoryManagerPass]

def parse(file: ir.File):
    info(f'Parsing file {file.path.as_posix()}')
    ir_builder = IRBuilder(file)
    program = ir_builder.build()
    if not file.options.no_stdlib:
        program.nodes.insert(0, ir.Use(program.pos, 'core'))
    
    return program

def run_compile_passes(file: ir.File):
    program = parse(file)
    ir_file = file.path.with_stem(f'{file.path.stem}_base').with_suffix('.gir')
    if file.options.debug:
        ir_file.write_text(str(program))
    
    for i, cls in enumerate(PASSES, start=1):
        info(f'Running pass {i}: {cls.__name__} on file {file.path.as_posix()}')
        program = cls.run(file, program)
        if file.options.debug:
            ir_file = file.path.with_stem(f'{file.path.stem}_pass{i}').with_suffix('.gir')
            ir_file.write_text(str(program))
        
        info(f'Successfully ran pass {i}: {cls.__name__} on file {file.path.as_posix()}')
    
    return program

def compile_to_str(file: ir.File):
    program = run_compile_passes(file)
    return CodeGenerationPass.run(file, program)

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
    
    return exe_file

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
    
    def action_test(self):
        test_name = self.arg(1)
        if test_name is None:
            self.error("""Usage: gem test <name>
No test name""")
        
        path = TESTS_DIR / f'{test_name}.gem'
        if not path.exists():
            self.error(f"""Usage: gem test <name>
No test named \'{test_name}\'""")
        
        exe_file = self.action_build(str(path))
        run(f'{exe_file}', shell=True)
    
    def action_build(self, file_path: str | None = None, options: ir.CompileOptions | None = None):
        if file_path is None:
            file_path = self.arg(1)
        
        if file_path is None:
            self.error("""Usage: gem build <file>
No file""")
        
        path = Path(file_path)
        if not path.exists():
            self.error(f"""Usage: gem build <file>
File \'{path}\' does not exist""")
        
        if not path.is_file():
            self.error(f"""Usage: gem build <file>
File \'{path}\' is not a file""")
        
        options = options or ir.CompileOptions(
            self.option('clean'), self.option('optimize'), self.option('debug'), self.option('no-stdlib')
        )
        
        file = ir.File(path, ir.Scope(), options)
        return compile_to_exe(file)
