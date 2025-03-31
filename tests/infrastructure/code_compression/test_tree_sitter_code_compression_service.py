import os
import unittest
from src.infrastructure.code_compression.tree_sitter_code_compression_service import TreeSitterCodeCompressionService
from src.model.value_objects.files_dictionary import FilesDictionary


class TestTreeSitterCodeCompressionService(unittest.TestCase):
    """
    Tests for the TreeSitterCodeCompressionService class.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.service = TreeSitterCodeCompressionService()

    def test_compress_empty_files_dictionary(self):
        """
        Test compressing an empty FilesDictionary.
        """
        files = FilesDictionary()
        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 0)

    def test_compress_non_python_files(self):
        """
        Test compressing a FilesDictionary with non-Python files.
        """
        files = FilesDictionary()
        files.add_file("test.txt", "This is a text file")
        files.add_file("test.md", "# Markdown file")

        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 0)

    def test_compress_python_file_without_classes(self):
        """
        Test compressing a Python file without any classes.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
def main():
    print("Hello, world!")
    
if __name__ == "__main__":
    main()
""")

        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 0)

    def test_compress_python_file_with_class_no_constructor(self):
        """
        Test compressing a Python file with a class but no constructor.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
class TestClass:
    \"\"\"A test class.\"\"\"
    
    def method(self):
        pass
""")

        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 1)
        self.assertIn("test.py", result.files)

        # The result should contain the class declaration and a pass statement
        compressed = result.files["test.py"]
        self.assertIn("class TestClass:", compressed)
        self.assertIn("    pass", compressed)
        self.assertNotIn("def method", compressed)

    def test_compress_python_file_with_class_and_constructor(self):
        """
        Test compressing a Python file with a class and constructor.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
class TestClass:
    \"\"\"A test class.\"\"\"
    
    def __init__(self, param1, param2="default"):
        \"\"\"Constructor for TestClass.\"\"\"
        self.param1 = param1
        self.param2 = param2
        
    def method(self):
        pass
""")

        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 1)
        self.assertIn("test.py", result.files)

        # The result should contain the class declaration and constructor signature
        compressed = result.files["test.py"]
        self.assertIn("class TestClass:", compressed)
        self.assertIn('def __init__(self, param1, param2="default"):', compressed)
        self.assertIn('"""Constructor for TestClass."""', compressed)
        self.assertNotIn("self.param1 = param1", compressed)
        self.assertNotIn("def method", compressed)

    def test_compress_python_file_with_multiple_classes(self):
        """
        Test compressing a Python file with multiple classes.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
class Class1:
    \"\"\"First class.\"\"\"
    
    def __init__(self):
        pass
        
class Class2:
    \"\"\"Second class.\"\"\"
    
    def __init__(self, param):
        \"\"\"Constructor for Class2.\"\"\"
        self.param = param
        
class Class3:
    \"\"\"Third class without constructor.\"\"\"
    
    def method(self):
        pass
""")

        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 1)
        self.assertIn("test.py", result.files)

        # The result should contain all three class declarations with appropriate constructors
        compressed = result.files["test.py"]
        self.assertIn("class Class1:", compressed)
        self.assertIn("def __init__(self):", compressed)
        self.assertIn("class Class2:", compressed)
        self.assertIn("def __init__(self, param):", compressed)
        self.assertIn('"""Constructor for Class2."""', compressed)
        self.assertIn("class Class3:", compressed)
        self.assertNotIn("def method", compressed)

    def test_compress_multiple_python_files(self):
        """
        Test compressing multiple Python files.
        """
        files = FilesDictionary()
        files.add_file("file1.py", """
class File1Class:
    def __init__(self, param):
        self.param = param
""")
        files.add_file("file2.py", """
class File2Class:
    def method(self):
        pass
""")
        files.add_file("file3.txt", "Not a Python file")

        result = self.service.compress_to_constructor_signatures(files)
        self.assertEqual(len(result.files), 2)
        self.assertIn("file1.py", result.files)
        self.assertIn("file2.py", result.files)
        self.assertNotIn("file3.txt", result.files)

        # Check file1.py content
        self.assertIn("def __init__(self, param):", result.files["file1.py"])

        # Check file2.py content
        self.assertIn("class File2Class:", result.files["file2.py"])
        self.assertIn("    pass", result.files["file2.py"])

    def test_compress_generator_service_py(self):
        files = FilesDictionary()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generator_service.py'), 'r') as f:
            files.add_file("generator_service.py", f.read())

        result = self.service.compress_to_constructor_signatures(files)

        result_file = result.files["generator_service.py"]
        self.assertIn("command_repository: CommandRepository,", result_file)
        self.assertIn("model_requirement_repository: ModelRequirementRepository,", result_file)
        self.assertIn("application_generator: ApplicationGenerator,", result_file)
        self.assertIn("domain_model_generator: DomainModelGenerator,", result_file)
        self.assertIn("application_files_service: ApplicationFilesService,", result_file)
        self.assertIn("domain_model_files_service: DomainModelFilesService", result_file)
        print(result_file)

    def test_remove_method_bodies_empty_files_dictionary(self):
        """
        Test removing method bodies from an empty FilesDictionary.
        """
        files = FilesDictionary()
        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 0)

    def test_remove_method_bodies_non_python_files(self):
        """
        Test removing method bodies from non-Python files.
        """
        files = FilesDictionary()
        files.add_file("test.txt", "This is a text file")
        files.add_file("test.md", "# Markdown file")

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 2)
        self.assertEqual(result.files["test.txt"], "This is a text file")
        self.assertEqual(result.files["test.md"], "# Markdown file")

    def test_remove_method_bodies_python_file_without_methods(self):
        """
        Test removing method bodies from a Python file without any methods.
        """
        files = FilesDictionary()
        content = """
# This is a Python file without methods
x = 10
y = 20
result = x + y
"""
        files.add_file("test.py", content)

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 1)
        self.assertEqual(result.files["test.py"], content)

    def test_remove_method_bodies_simple_function(self):
        """
        Test removing method bodies from a simple function.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
def simple_function():
    print("Hello, world!")
    return 42
""")

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 1)
        self.assertIn("def simple_function():", result.files["test.py"])
        self.assertIn("    pass", result.files["test.py"])
        self.assertNotIn('print("Hello, world!")', result.files["test.py"])
        self.assertNotIn("return 42", result.files["test.py"])

    def test_remove_method_bodies_function_with_docstring(self):
        """
        Test removing method bodies from a function with a docstring.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
def function_with_docstring():
    \"\"\"This is a docstring.\"\"\"
    print("Hello, world!")
    return 42
""")

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 1)
        self.assertEqual("""
def function_with_docstring():
    \"\"\"This is a docstring.\"\"\"
    pass
""", result.files["test.py"])

    def test_remove_method_bodies_class_with_methods(self):
        """
        Test removing method bodies from a class with methods.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
class TestClass:
    \"\"\"A test class.\"\"\"
    
    def __init__(self, param1, param2="default"):
        \"\"\"Constructor for TestClass.\"\"\"
        self.param1 = param1
        self.param2 = param2
        
    def method(self):
        print("This is a method")
        return self.param1
""")

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 1)

        # Check that class definition and docstring are preserved
        self.assertIn('class TestClass:', result.files["test.py"])
        self.assertIn('    """A test class."""', result.files["test.py"])

        # Check that constructor signature and docstring are preserved
        self.assertIn('    def __init__(self, param1, param2="default"):', result.files["test.py"])
        self.assertIn('        """Constructor for TestClass."""', result.files["test.py"])

        # Check that method signature is preserved
        self.assertIn('    def method(self):', result.files["test.py"])

        # Check that method bodies are replaced with pass
        self.assertIn('        pass', result.files["test.py"])

        # Check that method body content is removed
        self.assertNotIn('self.param1 = param1', result.files["test.py"])
        self.assertNotIn('self.param2 = param2', result.files["test.py"])
        self.assertNotIn('print("This is a method")', result.files["test.py"])
        self.assertNotIn('return self.param1', result.files["test.py"])

    def test_remove_method_bodies_multiple_classes(self):
        """
        Test removing method bodies from multiple classes.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
class Class1:
    def method1(self):
        return "Class1.method1"
        
class Class2:
    def method2(self):
        \"\"\"Method 2 docstring.\"\"\"
        return "Class2.method2"
""")

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 1)

        # Check that all class definitions are preserved
        self.assertIn('class Class1:', result.files["test.py"])
        self.assertIn('class Class2:', result.files["test.py"])

        # Check that all method signatures are preserved
        self.assertIn('    def method1(self):', result.files["test.py"])
        self.assertIn('    def method2(self):', result.files["test.py"])

        # Check that docstring is preserved
        self.assertIn('        """Method 2 docstring."""', result.files["test.py"])

        # Check that method bodies are replaced with pass
        self.assertIn('        pass', result.files["test.py"])

        # Check that method body content is removed
        self.assertNotIn('return "Class1.method1"', result.files["test.py"])
        self.assertNotIn('return "Class2.method2"', result.files["test.py"])

    def test_remove_method_bodies_nested_functions(self):
        """
        Test removing method bodies from nested functions.
        """
        files = FilesDictionary()
        files.add_file("test.py", """
def outer_function():
    print("Outer function")
    
    def inner_function():
        print("Inner function")
        return "inner"
        
    result = inner_function()
    return result
""")

        result = self.service.remove_method_bodies(files)
        self.assertEqual(len(result.files), 1)

        # Check that outer function signature is preserved
        self.assertIn('def outer_function():', result.files["test.py"])

        # Check that inner function is removed (part of outer function body)
        self.assertNotIn('def inner_function():', result.files["test.py"])

        # Check that outer function body is replaced with pass
        self.assertIn('    pass', result.files["test.py"])

        # Check that all function body content is removed
        self.assertNotIn('print("Outer function")', result.files["test.py"])
        self.assertNotIn('print("Inner function")', result.files["test.py"])
        self.assertNotIn('result = inner_function()', result.files["test.py"])
        self.assertNotIn('return result', result.files["test.py"])


if __name__ == "__main__":
    unittest.main()
