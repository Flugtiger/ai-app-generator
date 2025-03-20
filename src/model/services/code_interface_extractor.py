
import re
from typing import Dict, Optional
from src.model.value_objects.files_dictionary import FilesDictionary


class CodeInterfaceExtractor:
    """
    Service that extracts interfaces (class and public method declarations) from source code files.
    """

    # Language-specific patterns for class declarations
    CLASS_PATTERNS = {
        'py': r'class\s+(\w+)(?:\(.*?\))?:',
        'java': r'(?:public|protected|private)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+\w+)?(?:\s+implements\s+[\w,\s]+)?\s*\{',
        'js': r'(?:export\s+)?(?:default\s+)?class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{',
        'ts': r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:<.*?>)?(?:\s+extends\s+\w+)?(?:\s+implements\s+[\w,\s<>]+)?\s*\{',
        'cs': r'(?:public|protected|private|internal)?\s*(?:abstract|sealed)?\s*class\s+(\w+)(?:<.*?>)?(?:\s*:\s*[\w,\s<>]+)?\s*\{',
    }

    # Language-specific patterns for public method declarations
    METHOD_PATTERNS = {
        'py': r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\(.*?\))?(?:\s*->.*?)?\s*:',
        'java':
        r'(?:public|protected)\s+(?:static\s+)?(?:<.*?>)?\s*(?:\w+)\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\(.*?\))\s*(?:throws\s+[\w,\s]+)?\s*\{',
        'js': r'(?:async\s+)?(?:static\s+)?([a-zA-Z_][a-zA-Z0-9_]*)(?:\(.*?\))\s*\{',
        'ts': r'(?:public|protected)\s+(?:async\s+)?(?:static\s+)?([a-zA-Z_][a-zA-Z0-9_]*)(?:\(.*?\))(?:\s*:\s*.*?)?\s*\{',
        'cs':
        r'(?:public|protected)\s+(?:async\s+)?(?:static\s+)?(?:virtual\s+)?(?:override\s+)?(?:abstract\s+)?(?:\w+)\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\(.*))(?:\s*=>\s*.*?;|\s*\{)',
    }

    # Language-specific patterns for interface declarations
    INTERFACE_PATTERNS = {
        'java': r'(?:public)?\s*interface\s+(\w+)(?:\s+extends\s+[\w,\s]+)?\s*\{',
        'ts': r'(?:export\s+)?interface\s+(\w+)(?:<.*?>)?(?:\s+extends\s+[\w,\s<>]+)?\s*\{',
        'cs': r'(?:public|internal)?\s*interface\s+(\w+)(?:<.*?>)?(?:\s*:\s*[\w,\s<>]+)?\s*\{',
    }

    # Language-specific patterns for property declarations
    PROPERTY_PATTERNS = {
        'py': r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=',
        'java': r'(?:public|protected)\s+(?:final\s+)?(?:\w+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:=|;)',
        'ts': r'(?:public|protected)\s+(?:readonly\s+)?([a-zA-Z_][a-zA-Z0-9_]*)(?:\s*:\s*.*?)?\s*(?:=|;)',
        'cs': r'(?:public|protected)\s+(?:\w+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:\{|=>|=|;)',
    }

    @staticmethod
    def detect_language(file_path: str) -> Optional[str]:
        """                                                                                                                                   
        Detects the programming language based on file extension.                                                                             

        Args:                                                                                                                                 
            file_path: The path of the file.                                                                                                  

        Returns:                                                                                                                              
            The language code or None if not recognized.                                                                                      
        """
        extension = file_path.split('.')[-1].lower()

        language_map = {
            'py': 'py',
            'java': 'java',
            'js': 'js',
            'jsx': 'js',
            'ts': 'ts',
            'tsx': 'ts',
            'cs': 'cs',
        }

        return language_map.get(extension)

    @staticmethod
    def extract_interface(file_path: str, content: str) -> str:
        """                                                                                                                                   
        Extracts the interface (class and public method declarations) from a source code file.                                                

        Args:                                                                                                                                 
            file_path: The path of the file.                                                                                                  
            content: The content of the file.                                                                                                 

        Returns:                                                                                                                              
            The extracted interface.                                                                                                          
        """
        language = CodeInterfaceExtractor.detect_language(file_path)
        if not language:
            # If language not recognized, return the original content
            return content

        # Split the content into lines
        lines = content.split('\n')
        result_lines = []

        # Get the patterns for the detected language
        class_pattern = CodeInterfaceExtractor.CLASS_PATTERNS.get(language)
        method_pattern = CodeInterfaceExtractor.METHOD_PATTERNS.get(language)
        interface_pattern = CodeInterfaceExtractor.INTERFACE_PATTERNS.get(language)
        property_pattern = CodeInterfaceExtractor.PROPERTY_PATTERNS.get(language)

        # Process each line
        in_class = False
        in_method = False
        method_indent = 0
        brace_count = 0

        for line in lines:
            # Check if this line contains a class declaration
            if class_pattern and re.search(class_pattern, line):
                in_class = True
                result_lines.append(line)
                if '{' in line:
                    brace_count += line.count('{') - line.count('}')
                continue

            # Check if this line contains an interface declaration
            if interface_pattern and re.search(interface_pattern, line):
                in_class = True
                result_lines.append(line)
                if '{' in line:
                    brace_count += line.count('{') - line.count('}')
                continue

            # If we're in a class, check for method declarations
            if in_class:
                # Update brace count
                if '{' in line or '}' in line:
                    brace_count += line.count('{') - line.count('}')

                    # If brace count is 0 and we were in a class, we're now out of it
                    if brace_count == 0 and language != 'py':
                        in_class = False
                        result_lines.append(line)
                        continue

                indent = len(line) - len(line.lstrip())
                if in_method and language == 'py' and indent == method_indent:
                    in_method = False

                # Check if this line contains a method declaration
                if method_pattern and re.search(method_pattern, line):
                    in_method = True
                    method_indent = indent

                    # For Python, add the method declaration and a pass statement
                    if language == 'py':
                        result_lines.append(line)
                        result_lines.append(' ' * (method_indent + 4) + 'pass')
                    else:
                        # For other languages, add the method declaration
                        result_lines.append(line)

                        # If the method is a one-liner (has both { and } on the same line)
                        if '{' in line and '}' in line and line.rfind('{') < line.rfind('}'):
                            in_method = False
                    continue

                # Check if this line contains a property declaration
                if property_pattern and re.search(property_pattern, line) and not in_method:
                    result_lines.append(line)
                    continue

                # If we're in a method, check if we're exiting it
                if in_method:
                    if language != 'py':
                        # For non-Python languages, check for closing braces
                        if '}' in line:
                            result_lines.append(line)
                            in_method = False
                    continue

                # For Python, check for class-level indentation to determine if we're still in the class
                if language == 'py':
                    if line.strip() and not line.startswith(' '):
                        in_class = False
                    elif not line.strip():
                        result_lines.append(line)
                else:
                    # For non-Python languages, add class structure lines
                    if (line.strip() in ['{', '}'] or
                            line.strip().startswith('//') or
                            line.strip().startswith('/*') or
                            line.strip().startswith('*')):
                        result_lines.append(line)
            else:
                # If we're not in a class, add the line if it's not a method implementation
                if (not line.strip() or line.strip().startswith('import') or
                        line.strip().startswith('using') or
                        line.strip().startswith('package') or
                        line.strip().startswith('namespace')):
                    result_lines.append(line)

        return '\n'.join(result_lines)

    @staticmethod
    def extract_interfaces(files_dict: FilesDictionary) -> FilesDictionary:
        """                                                                                                                                   
        Extracts interfaces from all files in a FilesDictionary.                                                                              

        Args:                                                                                                                                 
            files_dict: The FilesDictionary containing source code files.                                                                     

        Returns:                                                                                                                              
            A new FilesDictionary with interface-only versions of the files.                                                                  
        """
        result = FilesDictionary()

        for file_path, content in files_dict.files.items():
            interface_content = CodeInterfaceExtractor.extract_interface(file_path, content)
            result.add_file(file_path, interface_content)

        return result
