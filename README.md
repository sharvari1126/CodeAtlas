# CodeAtlas

Repository Intelligence Copilot

## Features

- Clone GitHub repositories
- Analyze repository structure
- Extract functions using AST
- Extract classes using AST
- Generate repository tree

## Tech Stack

- Python
- FastAPI
- GitPython
- AST
- HTML
- Bootstrap
- JavaScript

## How It Works

1. User enters GitHub repository URL
2. Repository is cloned locally
3. Files are scanned
4. AST parses Python files
5. Functions/classes are extracted
6. Results displayed in UI

## Future Improvements

- Interactive tree
- Call graph generation
- Dependency analysis
- AI-powered repository summaries

## Installation

git clone https://github.com/sharvarii1126/CodeAtlas.git

cd CodeAtlas

pip install -r requirements.txt

uvicorn backend.main:app --reload
