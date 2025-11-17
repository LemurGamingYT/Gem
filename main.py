from logging import basicConfig, info, DEBUG
from sys import argv

from llvmlite import binding as llvm
from colorama import init

from gem import ArgParser, VERSION


def main():
    info(f'Bundle v{VERSION}')
    info('Backend: llvmlite/LLVM')
    info(f'Target: {llvm.get_default_triple()}')
    
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    
    arg_parser = ArgParser(argv[1:])
    arg_parser.parse()


if __name__ == '__main__':
    init()
    basicConfig(
        filename='debug.log', filemode='w',
        format='%(filename)s (line %(lineno)d) [%(levelname)s] - %(message)s',
        encoding='utf-8', level=DEBUG
    )
    main()
