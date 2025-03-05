from sys import argv

from colorama import init

from gem.arg_parser import GemArgParser


def main():
    arg_parser = GemArgParser(argv[1:])
    arg_parser.parse()


if __name__ == '__main__':
    init()
    main()
