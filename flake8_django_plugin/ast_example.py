import ast
from pathlib import Path

R = '************************************************************************************************************************************************'
class MyNodeVisitor(ast.NodeVisitor):
    def visit(self, node: ast.AST):
        print(node)
        self.generic_visit(node)


def parse_models_file(filename: Path):
    with open(filename) as model_file:
        code = model_file.read()
    node = ast.parse(code)

    node_visitor = MyNodeVisitor()
    node_visitor.visit(node)
    # print(node)
    # print('-' * 120)
    # print(node.body)
