import re
from typing import List, Optional

from tree_sitter import Language, Parser
from tree_sitter_language_pack import get_parser

from src.model.files.files_dictionary import FilesDictionary
from src.model.services.code_compressor import CodeCompressor


class CodeCompressorImpl(CodeCompressor):
    """
    Implementation of CodeCompressor using tree-sitter to extract class declarations and constructor signatures.
    """

    def __init__(self):
        """
        Initialize the code compressor with tree-sitter parser for Python.
        """
        self.parser = get_parser('python')

    def _extract_class_declarations(self, source_code: str) -> str:
        """
        Extract class declarations and constructor signatures from Python code.
        """
        tree = self.parser.parse(bytes(source_code, 'utf8'))
        root_node = tree.root_node

        # Find all class definitions
        class_nodes = []
        self._find_nodes_by_type(root_node, "class_definition", class_nodes)

        result = []

        # Process imports first
        import_lines = []
        for line in source_code.split('\n'):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line)

        if import_lines:
            result.extend(import_lines)
            result.append('')  # Add a blank line after imports

        # Process each class
        for class_node in class_nodes:
            class_text = source_code[class_node.start_byte:class_node.end_byte]
            class_lines = class_text.split('\n')

            # Get class definition line
            class_def_line = class_lines[0]
            result.append(class_def_line)

            # Find constructor method
            constructor_node = None
            for child in class_node.children:
                if child.type == "block":
                    function_nodes = []
                    self._find_nodes_by_type(child, "function_definition", function_nodes)
                    for func_node in function_nodes:
                        func_text = source_code[func_node.start_byte:func_node.end_byte]
                        if "__init__" in func_text.split('\n')[0]:
                            constructor_node = func_node
                            break

            # Process constructor if found
            if constructor_node:
                constructor_text = source_code[constructor_node.start_byte:constructor_node.end_byte]
                constructor_lines = constructor_text.split('\n')

                # Get constructor signature (first line and any parameter lines)
                signature_lines = [constructor_lines[0]]

                # Find the parameter list node
                param_list_node = None
                for child in constructor_node.children:
                    if child.type == "parameters":
                        param_list_node = child
                        break

                if param_list_node:
                    param_text = source_code[param_list_node.start_byte:param_list_node.end_byte]
                    param_lines = param_text.split('\n')

                    # If parameters span multiple lines, add them
                    if len(param_lines) > 1:
                        for i in range(1, len(constructor_lines)):
                            if ')' in constructor_lines[i]:
                                signature_lines.append(constructor_lines[i])
                                break
                            signature_lines.append(constructor_lines[i])

                # Add constructor body placeholder
                signature_lines.append("        pass")

                # Add constructor to result
                result.extend(["    " + line for line in signature_lines])

            # Add class methods as stubs
            for child in class_node.children:
                if child.type == "block":
                    function_nodes = []
                    self._find_nodes_by_type(child, "function_definition", function_nodes)
                    for func_node in function_nodes:
                        func_text = source_code[func_node.start_byte:func_node.end_byte]
                        func_lines = func_text.split('\n')

                        # Skip constructor as it's already processed
                        if "__init__" in func_lines[0]:
                            continue

                        # Add method signature and placeholder
                        result.append("    " + func_lines[0])
                        result.append("        pass")

            # Add a blank line after each class
            result.append('')

        return '\n'.join(result)

    def _find_nodes_by_type(self, node, type_name: str, result: List):
        """
        Recursively find nodes of a specific type in the syntax tree.
        """
        if node.type == type_name:
            result.append(node)

        for child in node.children:
            self._find_nodes_by_type(child, type_name, result)

    def compress(self, files_dict: FilesDictionary) -> FilesDictionary:
        """
        Takes a FilesDictionary as parameter and returns a FilesDictionary where the file contents
        have been reduced to class declarations and constructor signatures.
        """
        compressed_files = FilesDictionary()

        for path, content in files_dict.get_all_files().items():
            if path.endswith('.py'):
                compressed_content = self._extract_class_declarations(content)
                compressed_files.add_file(path, compressed_content)
            else:
                # For non-Python files, keep the original content
                compressed_files.add_file(path, content)

        return compressed_files
