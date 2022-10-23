import ast
from pathlib import Path


def parse_models_file(filename: Path):
    with open(filename) as model_file:
        code = model_file.read()
    node = ast.parse(code)

    print(node)
    print('-' * 120)
    print(node.body)
