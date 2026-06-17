from git import Repo
import os
import ast

def clone_repository(repo_url):

    repo_name = repo_url.split("/")[-1].replace(".git", "")

    clone_path = os.path.join("repositories", repo_name)

    if os.path.exists(clone_path):
        return clone_path

    Repo.clone_from(repo_url, clone_path)

    return clone_path


def scan_repository(repo_path):

    all_files = []
    python_files = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

            if file.endswith(".py"):
                python_files.append(file_path)

    return {
    "total_files": len(all_files),
    "python_files": len(python_files)
}
    

def extract_code_structure(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    functions = []
    classes = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return {
        "functions": functions,
        "classes": classes
    }


def find_definitions(repo_path):

    definitions = []

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)

            try:

                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()

                tree = ast.parse(source)

                for node in ast.walk(tree):

                    if isinstance(node, ast.FunctionDef):

                        definitions.append({
                            "type": "function",
                            "name": node.name,
                            "file": file,
                            "line": node.lineno
                        })

                    elif isinstance(node, ast.ClassDef):

                        definitions.append({
                            "type": "class",
                            "name": node.name,
                            "file": file,
                            "line": node.lineno
                        })

            except Exception:
                pass

    return definitions[:50]


def build_repository_tree(repo_path):


    tree = []

    for root, dirs, files in os.walk(repo_path):
        ignore_dirs = {
    ".git",
    ".github",
    ".devcontainer",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".idea",
    ".vscode"
}

        dirs[:] = [
            d for d in dirs
            if d not in ignore_dirs
        ]


        level = root.replace(repo_path, "").count(os.sep)

        indent = "│   " * level

        tree.append(
            f"{indent}{os.path.basename(root)}/"
        )

        sub_indent = "│   " * (level + 1)

        for file in files:

            tree.append(
                f"{sub_indent}{file}"
            )

    return tree


def analyze_repository(repo_path):

    scan_results = scan_repository(repo_path)

    definitions = find_definitions(repo_path)

    functions = set()
    classes = set()
    tree = build_repository_tree(repo_path)

    for item in definitions:

        if item["type"] == "function":
            functions.add(item["name"])

        elif item["type"] == "class":
            classes.add(item["name"])

    return {
        "total_files": scan_results["total_files"],
        "python_files": scan_results["python_files"],
        "functions": list(functions),
        "classes": list(classes),
        "definitions": definitions,
        "repository_tree": tree 

    }