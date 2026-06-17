import ast

with open("astcheck.py", "r") as file:
    source = file.read()

tree = ast.parse(source)

for node in ast.walk(tree):

    if isinstance(node, ast.FunctionDef):
        print(node.name)
        print(node.lineno)

    if isinstance(node, ast.ClassDef):
        print(node.name)
        print(node.lineno)