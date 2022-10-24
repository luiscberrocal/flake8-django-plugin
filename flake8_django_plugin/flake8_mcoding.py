import ast
from typing import NamedTuple


class Flake8ASTErrorInfo(NamedTuple):
    line_number: int
    offset: int
    msg: str
    cls: type


class MCodingASTPlugin:
    name = 'flake8_mcoding_ast'
    version = '0.0.0'

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self):
        print('Running')
        yield Flake8ASTErrorInfo(2, 3, 'MCOD100 Alwas error', type(self))





