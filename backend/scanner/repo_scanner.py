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


def analyze_repository(repo_path):

    scan_results = scan_repository(repo_path)

    definitions = find_definitions(repo_path)

    functions = []
    classes = []

    for item in definitions:

        if item["type"] == "function":
            functions.append(item["name"])

        elif item["type"] == "class":
            classes.append(item["name"])

    return {
        "total_files": scan_results["total_files"],
        "python_files": scan_results["python_files"],
        "functions": functions,
        "classes": classes,
        "definitions": definitions
    }