import ast
import unittest
import coverage
import os
import glob
import sys
import networkx as nx
import random
from dotenv import load_dotenv

load_dotenv()
folder_name = os.getenv("FOLDER_NAME")


class TestCaseGenerator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.test_cases = []
        self.test_dir = f"test_{os.path.basename(self.folder_path)}"

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def generate_tests_for_directory(self):
        python_files = glob.glob(os.path.join(self.folder_path, "*.py"))
        for file in python_files:
            if os.path.basename(file).startswith("__init__"):
                continue  
            print(f"Generating tests for {file}")
            self.tree = self.parse_file(file)
            self.generate_tests_for_file(file)
            self.write_tests_to_file(file)

    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            source = file.read()
        return ast.parse(source)

    def generate_tests_for_file(self, file_name):
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.generate_test_for_function(node, base_name)
                self.analyze_function_complexity(node)

    def generate_test_for_function(self, func_node, base_name):
        test_name = f'test_{func_node.name}'
        arguments = self.get_function_arguments(func_node)
        args_values = self.generate_default_values_for_args(arguments)

        test_case = f"""
    def {test_name}(self):
        # Test for {func_node.name} in {base_name}
        result = {func_node.name}({', '.join(args_values)})  # Replace with actual arguments
        self.assertEqual(result, None)  # Replace with actual expected value
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
            if arg in ('a', 'b'):  
                default_values.append(str(random.randint(1, 10)))  
            elif arg.lower() in ('name', 'title', 'key'):  
                default_values.append(f'"{arg}_example"')  
            else:
                default_values.append('"default_value"')  
        return default_values

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
            file.write(f"sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{folder_name}')))\n")
            file.write(f"\nfrom {os.path.basename(self.folder_path)}.{os.path.splitext(os.path.basename(file_name))[0]} import *\n")
            file.write(f"\nclass Test{os.path.splitext(os.path.basename(file_name))[0].capitalize()}(unittest.TestCase):\n")
            if not self.test_cases:
                file.write("    def test_placeholder(self):\n")
                file.write("        pass\n")
            for test_case in self.test_cases:
                file.write(test_case)
            self.test_cases.clear()

    def infer_types(self, func_node):
        for stmt in func_node.body:
            if isinstance(stmt, ast.AnnAssign):
                print(f"Type annotation: {stmt.target.id} -> {ast.dump(stmt.annotation)}")
            elif isinstance(stmt, ast.Assign):
                print(f"Assignment: {stmt.targets[0].id} = {ast.dump(stmt.value)}")

    def run_tests_and_generate_coverage(self):
        cov = coverage.Coverage()
        cov.start()
        unittest.TextTestRunner().run(unittest.defaultTestLoader.discover(self.test_dir))
        cov.stop()
        cov.save()
        cov.report()

    def run(self):
        self.generate_tests_for_directory()
        self.run_tests_and_generate_coverage()


if __name__ == '__main__':
    folder_path =  os.getenv('FOLDER_PATH')
    generator = TestCaseGenerator(folder_path)
    generator.run()
