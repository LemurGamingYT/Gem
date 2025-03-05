from subprocess import run
from pathlib import Path

from gem import compile, compile_cmake, GemCompileOptions
from gem.target import get_current_target


class GemArgParser:
    def __init__(self, args: list[str]):
        self.args = args
    
    def get_actions(self):
        actions = {}
        for k in dir(self):
            if not k.startswith('action_'):
                continue

            v = getattr(self, k)
            if callable(v):
                actions[k.removeprefix('action_')] = v
        
        return actions
    
    def flag(self, one_dash_name: str | None = None, double_dash_name: str | None = None):
        if one_dash_name is not None and f'-{one_dash_name}' in self.args:
            return True
        
        if double_dash_name is not None and f'--{double_dash_name}' in self.args:
            return True
        
        return False
    
    def value_of(self, one_dash_name: str | None = None, double_dash_name: str | None = None):
        if one_dash_name is not None and f'-{one_dash_name}' in self.args:
            i = self.args.index(f'-{one_dash_name}')
            try:
                return self.args[i + 1]
            except IndexError:
                return None

        if double_dash_name is not None and f'--{double_dash_name}' in self.args:
            i = self.args.index(f'--{double_dash_name}')
            try:
                return self.args[i + 1]
            except IndexError:
                return None

        return None
    
    def arg(self, i: int):
        if len(self.args) <= i:
            return None
        
        return self.args[i]
    
    def parse(self):
        action = self.arg(0)
        func = self.get_actions().get(action)
        if func is None:
            func = self.action_help
            print('invalid action')
        
        func()
    
    def action_help(self):
        """help - show this help message"""

        print('usage: gem <action> [args...]')
        print('actions:')
        actions = self.get_actions()
        for v in actions.values():
            print(f'  {v.__doc__}')
    
    def action_build(self):
        """build <file> - build the given file"""

        file = self.arg(1)
        if file is None:
            print('usage: gem build <file>')
            print('invalid file')
            return
        
        path = Path(file)
        if not path.exists():
            print('usage: gem build <file>')
            print('file does not exist')
            return

        options = GemCompileOptions(path, get_current_target(), debug=self.flag('dbg', 'debug'))
        compile(options)
    
    def action_test(self):
        """test <name> - test the given name"""

        name = self.arg(1)
        if name is None:
            print('usage: gem test <name>')
            print('invalid name')
            return
        
        test_dir = Path(__file__).parent.parent / 'testing' / name
        if not test_dir.exists():
            print(f'test \'{name}\' does not exist')
            return
        
        kwargs = {'-S': test_dir.as_posix(), '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY': test_dir.as_posix()}
        ret_code = compile_cmake(test_dir / 'CMakeBuild', **kwargs)
        if ret_code.returncode != 0:
            print(f'failed to build test \'{name}\'')
            return

        RUN_CMD = f'{(test_dir / "Debug" / f"{name}.exe").as_posix()}'
        run(RUN_CMD, shell=True)
