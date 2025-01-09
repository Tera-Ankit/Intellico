import ast
import unittest
import coverage
import os
import glob
import sys
import random
import importlib.util
import networkx as nx
from dotenv import load_dotenv
load_dotenv()
 
class TestCaseGenerator:
    def __init__(self, folder_path, output_folder):
        self.folder_path = folder_path
        self.test_cases = []
        self.test_dir = os.path.join(output_folder, f"test_{os.path.basename(self.folder_path)}")
 
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
 
    def generate_tests_for_directory(self):
        python_files = glob.glob(os.path.join(self.folder_path, "*.py"))
        for file in python_files:
            if os.path.basename(file).startswith("__init__"):
                continue  # Skip __init__.py files
            print(f"Generating tests for {file}")
            self.tree = self.parse_file(file)
            self.generate_tests_for_file(file)
            self.write_tests_to_file(file)
 
    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            source = file.read()
        return ast.parse(source)
 
    def generate_tests_for_file(self, file_name):
        self.current_file_path = file_name  # Set the current file path
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.generate_test_for_function(node, base_name)
                self.analyze_function_complexity(node)
 
    def generate_test_for_function(self, func_node, base_name):
        test_name = f'test_{func_node.name}'
        arguments = self.get_function_arguments(func_node)
        args_values = self.generate_default_values_for_args(arguments)
 
        # Handle the function with try-except for error handling
        try:
            # Execute the function to get the expected value
            expected_value = self.execute_function(func_node, args_values)
 
            test_case = f"""
    def {test_name}(self):
        # Test for {func_node.name} in {base_name}
        result = {func_node.name}({', '.join(args_values)})  # Replace with actual arguments
        self.assertEqual(result, {expected_value})  # Replace with actual expected value
"""
        except Exception as e:
            test_case = f"""
    def {test_name}(self):
        # Test for {func_node.name} in {base_name}
        with self.assertRaises({e.__class__.__name__}):
            {func_node.name}({', '.join(args_values)})
"""
        self.test_cases.append(test_case)
 
    def get_function_arguments(self, func_node):
        """Extracts arguments from function node."""
        arguments = []
        for arg in func_node.args.args:
            arguments.append(arg.arg)
        return arguments
 
    def generate_default_values_for_args(self, arguments):
        """Generates default values for function arguments."""
        default_values = []
        for arg in arguments:
            if arg in ('a', 'b'):  # Arithmetic function arguments
                default_values.append(str(random.randint(1, 10)))  # Integers
            elif arg.lower() in ('name', 'title', 'key'):  # String-based arguments
                default_values.append(f'"{arg}_example"')
            elif arg.lower() in ('file_path', 'file'):  # File-related arguments
                default_values.append('"dummy_file.txt"')  # Mock file path
            elif arg.lower() == 'exception':  # Error handling
                default_values.append('"ValueError"')  # Placeholder for error types
            else:
                default_values.append('"default_value"')  # Default string value
        return default_values
 
    def execute_function(self, func_node, args_values):
        """Executes the function with default arguments and returns the result."""
        func_code = ast.unparse(func_node)
        exec_globals = {}
        exec_locals = {}
 
        # Dynamically load the module
        file_path = self.current_file_path
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
 
        # Add the parent directory of the file to sys.path for relative imports
        parent_dir = os.path.abspath(os.path.dirname(file_path))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
 
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
 
        # Add the module's globals to exec_globals
        exec_globals.update(module.__dict__)
 
        # Execute the function code in the context
        exec(func_code, exec_globals, exec_locals)
 
        # Get the function from the context
        func = exec_locals[func_node.name]
 
        # Convert argument values from string to actual values
        args = self.convert_args_to_correct_types(func_node, args_values)
 
        # Execute the function with arguments and return the result
        return func(*args)
 
    def convert_args_to_correct_types(self, func_node, args_values):
        """Convert arguments to correct types based on the function signature."""
        converted_args = []
        for arg, value in zip(func_node.args.args, args_values):
            # Try to cast to int or float if necessary
            if isinstance(value, str):
                if value.isdigit():
                    converted_args.append(int(value))  # Convert to int if the string is a digit
                elif value.replace('.', '', 1).isdigit():  # For floats
                    converted_args.append(float(value))
                else:
                    converted_args.append(value)  # Keep string if it's not a digit
            else:
                converted_args.append(value)
        return converted_args
 
    def construct_cfg(self, func_node):
        cfg = nx.DiGraph()
        last_node = None
        for stmt in func_node.body:
            node_id = id(stmt)
            cfg.add_node(node_id, label=ast.dump(stmt))
            if last_node:
                cfg.add_edge(last_node, node_id)
            last_node = node_id
        return cfg
 
    def analyze_function_complexity(self, func_node):
        cfg = self.construct_cfg(func_node)
        edges = cfg.number_of_edges()
        nodes = cfg.number_of_nodes()
        complexity = edges - nodes + 2
        print(f"Cyclomatic complexity for function '{func_node.name}': {complexity}")
 
    def write_tests_to_file(self, file_name):
        test_file_name = os.path.join(self.test_dir, f"test_{os.path.basename(file_name)}")
        with open(test_file_name, 'w') as file:
            file.write("import unittest\n")
            file.write("import sys\n")
            file.write("import os\n")
            file.write(f"sys.path.append('{os.path.abspath(self.folder_path)}')\n")  # Add the folder path to sys.path
            file.write(f"\nfrom {os.path.splitext(os.path.basename(file_name))[0]} import *\n")
            file.write(f"\nclass Test{os.path.splitext(os.path.basename(file_name))[0].capitalize()}(unittest.TestCase):\n")
            if not self.test_cases:
                file.write("    def test_placeholder(self):\n")
                file.write("        pass\n")
            for test_case in self.test_cases:
                file.write(test_case)
            self.test_cases.clear()
 
    def run_tests_and_generate_coverage(self):
        coverage_file_path = os.path.join(self.test_dir, ".coverage")
        cov = coverage.Coverage(data_file=coverage_file_path)
        cov.start()
        unittest.TextTestRunner().run(unittest.defaultTestLoader.discover(self.test_dir))
        cov.stop()
        cov.save()
        cov.report()
 
    def run(self):
        self.generate_tests_for_directory()
        self.run_tests_and_generate_coverage()
 
 
if __name__ == '__main__':
    # path = input("Enter the path to the Python file or folder: ").strip()
    path = os.getenv("FOLDER_PATH")
   
    if os.path.isdir(path):
        generator = TestCaseGenerator(path, os.getenv("OUTPUT_FOLDER"))
        generator.run()
    elif os.path.isfile(path) and path.endswith(".py"):
        generator = TestCaseGenerator(os.path.dirname(path))
        generator.generate_tests_for_file(path)
        generator.write_tests_to_file(path)
    else:
        print("Invalid path. Please provide a valid Python file or folder.")