from typing import List, Optional

from src.model.services.code_compression_service import CodeCompressionService
from src.model.value_objects.files_dictionary import FilesDictionary

from tree_sitter_languages import get_parser


class TreeSitterCodeCompressionService(CodeCompressionService):
    """
    Implementation of CodeCompressionService using tree-sitter for parsing code.
    Currently only supports Python code.
    """

    def __init__(self):
        """
        Initialize the TreeSitterCodeCompressionService.
        Sets up the tree-sitter parser for Python.
        """
        # Initialize tree-sitter
        self._setup_parser()

    def _setup_parser(self):
        """
        Set up the tree-sitter parser for Python.
        Assumes tree-sitter-languages is installed via pip.
        """
        try:
            # Get the Python parser
            self.parser = get_parser('python')
        except ImportError:
            raise ImportError(
                "tree-sitter-languages package not found. "
                "Please install it with: pip install tree-sitter-languages"
            )

    def compress_to_constructor_signatures(self, files: FilesDictionary) -> FilesDictionary:
        """
        Compresses the given FilesDictionary so that only class declarations and constructor signatures are left in the source files.

        Args:
            files: A FilesDictionary with source code files.

        Returns:
            A FilesDictionary where only class declarations and constructor signatures are left in the contents of the files
        """
        result = FilesDictionary()

        for path, content in files.files.items():
            # Only process Python files
            if not path.endswith('.py'):
                continue

            # Parse the file
            tree = self.parser.parse(bytes(content, "utf8"))

            # Extract class declarations and constructor signatures
            compressed_content = self._extract_class_info(content, tree.root_node)

            # Only add the file if it contains class declarations
            if compressed_content.strip():
                result.add_file(path, compressed_content)

        return result

    def _extract_class_info(self, source_code: str, root_node) -> str:
        """
        Extract class declarations and constructor signatures from the parsed AST.

        Args:
            source_code: The original source code.
            root_node: The root node of the AST.

        Returns:
            A string containing only class declarations and constructor signatures.
        """
        result_parts = []

        # Find all class definitions
        class_nodes = self._find_nodes_by_type(root_node, "class_definition")

        for class_node in class_nodes:
            # Get the class name
            class_name_node = self._find_node_by_type(class_node, "identifier")
            if not class_name_node:
                continue

            # Extract just the class header (not the entire class body)
            class_header = self._extract_class_header(source_code, class_node)

            # Find the constructor method
            constructor = None
            function_defs = self._find_nodes_by_type(class_node, "function_definition")

            for func in function_defs:
                func_name = self._find_node_by_type(func, "identifier")
                if func_name and self._get_node_text(source_code, func_name) == "__init__":
                    constructor = func
                    break

            # Build the compressed class definition
            if constructor:
                # Get the constructor signature
                constructor_sig = self._get_constructor_signature(source_code, constructor)
                
                # Preserve indentation for multi-line signatures
                if '\n' in constructor_sig:
                    # Ensure proper indentation for multi-line signatures
                    constructor_sig = constructor_sig.replace('\n', '\n    ')

                # Get the constructor docstring if it exists
                docstring = self._get_docstring(source_code, constructor)

                # Add the class header and constructor signature to the result
                class_text = f"{class_header}\n    {constructor_sig}"
                if docstring:
                    class_text += f"\n        {docstring}\n        pass"
                else:
                    class_text += "\n        pass"

                result_parts.append(class_text)
            else:
                # If no constructor is found, add just the class header
                result_parts.append(f"{class_header}\n    pass")

        return "\n\n".join(result_parts)

    def _find_nodes_by_type(self, node, type_name: str) -> List:
        """
        Find all nodes of a specific type in the AST.

        Args:
            node: The node to search in.
            type_name: The type of nodes to find.

        Returns:
            A list of nodes of the specified type.
        """
        results = []

        if node.type == type_name:
            results.append(node)

        for child in node.children:
            results.extend(self._find_nodes_by_type(child, type_name))

        return results

    def _find_node_by_type(self, node, type_name: str) -> Optional:
        """
        Find the first node of a specific type in the AST.

        Args:
            node: The node to search in.
            type_name: The type of node to find.

        Returns:
            The first node of the specified type, or None if not found.
        """
        if node.type == type_name:
            return node

        for child in node.children:
            result = self._find_node_by_type(child, type_name)
            if result:
                return result

        return None

    def _get_node_text(self, source_code: str, node) -> str:
        """
        Get the text of a node from the source code.

        Args:
            source_code: The original source code.
            node: The node to get text for.

        Returns:
            The text of the node.
        """
        return source_code[node.start_byte:node.end_byte]

    def _get_constructor_signature(self, source_code: str, constructor_node) -> str:
        """
        Get the constructor signature from a constructor node.

        Args:
            source_code: The original source code.
            constructor_node: The constructor function node.

        Returns:
            The constructor signature as a string.
        """
        # Find the parameters node
        parameters = self._find_node_by_type(constructor_node, "parameters")

        if parameters:
            # Find the colon that marks the end of the signature
            func_text = source_code[constructor_node.start_byte:constructor_node.end_byte]
            
            # Find the block node that contains the function body
            block_node = self._find_node_by_type(constructor_node, "block")
            if block_node:
                # Get just the signature part (everything before the block)
                signature_text = source_code[constructor_node.start_byte:block_node.start_byte].strip()
                
                # Ensure it ends with a colon
                if not signature_text.endswith(':'):
                    signature_text += ':'
                    
                return signature_text
            
            # Fallback if we can't find the block
            colon_pos = func_text.find(':')
            if colon_pos != -1:
                return func_text[:colon_pos + 1]
                
            return func_text + ':'

        return "def __init__(self):"

    def _get_docstring(self, source_code: str, node) -> Optional[str]:
        """
        Get the docstring of a node if it exists.

        Args:
            source_code: The original source code.
            node: The node to get the docstring for.

        Returns:
            The docstring as a string, or None if no docstring exists.
        """
        # Find the function body
        body = None
        for child in node.children:
            if child.type == "block":
                body = child
                break

        if not body or not body.children:
            return None

        # Check if the first statement is a string (docstring)
        first_stmt = body.children[0]
        if first_stmt.type == "expression_statement":
            string_node = self._find_node_by_type(first_stmt, "string")
            if string_node:
                return self._get_node_text(source_code, string_node)

        return None

    def _extract_class_header(self, source_code: str, class_node) -> str:
        """
        Extract just the class header (class name, inheritance, etc.) without the body.

        Args:
            source_code: The original source code.
            class_node: The class definition node.

        Returns:
            The class header as a string.
        """
        # Find the colon that marks the end of the class header
        class_text = self._get_node_text(source_code, class_node)
        header_end = class_text.find(':') + 1
        class_header = class_text[:header_end]

        # Extract the docstring if it exists
        docstring = None
        body = None

        # Find the body block
        for child in class_node.children:
            if child.type == "block":
                body = child
                break

        if body and body.children:
            # Check if the first statement is a string (docstring)
            first_stmt = body.children[0]
            if first_stmt.type == "expression_statement":
                string_node = self._find_node_by_type(first_stmt, "string")
                if string_node:
                    docstring = self._get_node_text(source_code, string_node)

        # Add the docstring to the header if it exists
        if docstring:
            class_header += f"\n    {docstring}"

        return class_header
