import os
import subprocess
import sys
from pathlib import Path


def build_tree_sitter_languages():
    """
    Build the tree-sitter language library for Python.
    This script clones the tree-sitter-python repository if it doesn't exist
    and builds the language library.
    """
    # Get the directory of this script
    current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Path to the tree-sitter-python repository
    py_repo_path = current_dir / "tree-sitter-python"
    
    # Path to the compiled language library
    lib_path = current_dir / "tree-sitter-languages.so"
    
    # Clone the tree-sitter-python repository if it doesn't exist
    if not py_repo_path.exists():
        print("Cloning tree-sitter-python repository...")
        subprocess.run(
            ["git", "clone", "https://github.com/tree-sitter/tree-sitter-python.git"],
            cwd=current_dir,
            check=True
        )
    
    # Import tree_sitter to build the language library
    try:
        from tree_sitter import Language
    except ImportError:
        print("tree-sitter package not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "tree-sitter"], check=True)
        from tree_sitter import Language
    
    # Build the language library
    print("Building tree-sitter language library...")
    Language.build_library(
        str(lib_path),
        [str(py_repo_path)]
    )
    
    print(f"Tree-sitter language library built successfully at {lib_path}")


if __name__ == "__main__":
    build_tree_sitter_languages()
