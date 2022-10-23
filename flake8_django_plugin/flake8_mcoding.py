import ast


class MCodingASTPlugin:
    name = 'flake8_mcoding_ast'
    version = '0.0.0'

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self):
        print('Running')
        yield from []
