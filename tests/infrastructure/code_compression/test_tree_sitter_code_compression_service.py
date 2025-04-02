import os
import unittest
from src.infrastructure.services.code_compressor_impl import CodeCompressorImpl
from src.model.files.files_dictionary import FilesDictionary


class TestCodeCompressorImpl(unittest.TestCase):
    """
    Tests for the CodeCompressorImpl class.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        self.service = CodeCompressorImpl()

    def test_compress_empty_files_dictionary(self):
        """
        Test compressing an empty FilesDictionary.
        """
        files = FilesDictionary()
        result = self.service.compress(files)
        self.assertEqual(len(result.files), 0)

    def test_compress_non_python_files(self):
        """
        Test compressing a FilesDictionary with non-Python files.
        """
        files = FilesDictionary()
        files.add_file("test.txt", "This is a text file")
        files.add_file("test.md", "# Markdown file")

        result = self.service.compress(files)
        self.assertEqual(result, files)

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

        result = self.service.compress(files)
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

        result = self.service.compress(files)
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

        result = self.service.compress(files)
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

        result = self.service.compress(files)
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

        result = self.service.compress(files)
        self.assertEqual(len(result.files), 3)
        self.assertIn("file1.py", result.files)
        self.assertIn("file2.py", result.files)
        self.assertIn("file3.txt", result.files)

        # Check file1.py content
        self.assertIn("def __init__(self, param):", result.files["file1.py"])

        # Check file2.py content
        self.assertIn("class File2Class:", result.files["file2.py"])
        self.assertIn("    pass", result.files["file2.py"])

        # Check file3.txt content
        self.assertEqual(files.files["file3.txt"], result.files["file3.txt"])

    def test_compress_generator_service_py(self):
        files = FilesDictionary()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generator_service.py'), 'r') as f:
            files.add_file("generator_service.py", f.read())

        result = self.service.compress(files)

        result_file = result.files["generator_service.py"]
        self.assertIn("command_repository: CommandRepository,", result_file)
        self.assertIn("model_requirement_repository: ModelRequirementRepository,", result_file)
        self.assertIn("application_generator: ApplicationGenerator,", result_file)
        self.assertIn("domain_model_generator: DomainModelGenerator,", result_file)
        self.assertIn("application_files_service: ApplicationFilesService,", result_file)
        self.assertIn("domain_model_files_service: DomainModelFilesService", result_file)
        print(result_file)


if __name__ == "__main__":
    unittest.main()
