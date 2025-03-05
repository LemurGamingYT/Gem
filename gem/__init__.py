from dataclasses import dataclass
from pprint import pformat
from subprocess import run
from shutil import rmtree
from pathlib import Path

from colorama import Fore, Style

from gem.passes.code_generation import GemCodeGeneration
from gem.passes.memory_manager import MemoryManager
from gem.ir import Scope, Position, stdlib_path
from gem.passes.analyser import GemAnalyser
from gem.ir_builder import GemIRBuilder
from gem.passes import run_pass
from gem.target import Target


@dataclass
class GemCompileOptions:
    file: Path
    target: Target
    debug: bool = False

@dataclass
class GemCMakeCompileArgs:
    scope: Scope
    out_file: Path
    file: Path
    target: Target


def compile_cmake(build_dir: Path = Path.cwd(), **kwargs):
    kwargs_str = ' '.join(f'{k}={v}' for k, v in kwargs.items())
    make_build_cmd = f'cmake -B {build_dir.as_posix()} {kwargs_str}'
    build_cmd = f'cmake --build {build_dir.as_posix()}'
    return run(f'{make_build_cmd} && {build_cmd}', shell=True)

def compile_with_cmake(args: GemCMakeCompileArgs):
    build_dir = (args.file.parent / 'build').absolute()
    build_dir.mkdir(exist_ok=True)

    cmake_name = args.file.stem
    build_type = 'Debug'

    cmakelists = args.file.parent / 'CMakeLists.txt'
    cmakelists.write_text(f"""cmake_minimum_required(VERSION 3.10)
project({cmake_name} LANGUAGES C)

set(CMAKE_BUILD_TYPE "{build_type}")
set(CMAKE_C_STANDARD 11)
set(SOURCES {args.out_file.as_posix()}{''.join(' ' + arg for arg in args.scope.compile_args)})

include_directories({stdlib_path.as_posix()})

add_executable({cmake_name} ${{SOURCES}})

if(MSVC)
    target_compile_options({cmake_name} PRIVATE /W4)
else()
    target_compile_options({cmake_name} PRIVATE -Wall -Wextra -Wpedantic)
endif()

target_include_directories({cmake_name} PRIVATE {stdlib_path.as_posix()})

add_compile_definitions({args.target.macro_name}=1)
""")

    kwargs = {'-S': cmakelists.parent.as_posix()}
    ret_code = compile_cmake(build_dir, **kwargs)
    if ret_code.returncode != 0:
        print(f'{Fore.RED}error: failed to build{Style.RESET_ALL}')
        exit(1)

    exec_name = f'{cmake_name}.exe'
    exec_file = build_dir / 'Debug' / exec_name

    new_exec_path = args.file.parent / exec_name
    if new_exec_path.exists():
        new_exec_path.unlink()
    
    exec_file.rename(new_exec_path)

    args.out_file.unlink(missing_ok=True)
    cmakelists.unlink(missing_ok=True)
    rmtree(build_dir)

def compile(options: GemCompileOptions):
    scope = Scope.make_global(options.file, Position(1, 0))

    builder = GemIRBuilder(scope)
    program = builder.build()
    if options.debug:
        print(f'{Fore.MAGENTA}Base IR: {pformat(program)}{Style.RESET_ALL}')
    
    program = run_pass(GemAnalyser, program, scope)
    if options.debug:
        print(f'{Fore.GREEN}Analysed IR: {pformat(program)}{Style.RESET_ALL}')
    
    program = run_pass(MemoryManager, program, scope)
    if options.debug:
        print(f'{Fore.BLUE}Memory Managed IR: {pformat(program)}{Style.RESET_ALL}')
    
    out = run_pass(GemCodeGeneration, program, scope)
    out_file = (options.file.parent / 'main.c').absolute()
    out_file.write_text(out)

    args = GemCMakeCompileArgs(scope, out_file, options.file, options.target)
    compile_with_cmake(args)
