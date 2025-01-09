import os
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()

def generate_test_case(component_path, component_name, test_dir):
    component_dir = os.path.dirname(component_path)
    relative_path = os.path.relpath(component_dir, test_dir).replace(os.sep, "/")

    import_statement = (
        f"import {{ {component_name} }} from '{relative_path}/{component_name}';"
    )

    try:
        with open(component_path, "r") as f:
            content = f.read()
            if "export default" in content:
                import_statement = (
                    f"import {component_name} from '{relative_path}/{component_name}';"
                )
    except Exception as e:
        print(f"Error reading file {component_path}: {e}")

    test_content = f"""
import React from 'react';
import {{ render }} from '@testing-library/react';
{import_statement}

describe('{component_name}', () => {{
  it('renders correctly', () => {{
    expect({component_name}).toBeDefined();
    render(<{component_name} />);
  }});
}});
"""

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    test_file_path = os.path.join(test_dir, f"{component_name}.test.js")
    with open(test_file_path, "w") as f:
        f.write(test_content)

def generate_tests_for_folder(folder_path, test_dir):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".js") or file.endswith(".jsx"):
                component_path = os.path.join(root, file)
                component_name = os.path.splitext(file)[0]
                generate_test_case(component_path, component_name, test_dir)

def process_folder(folder_path, output_folder):
    test_dir = os.path.join(output_folder)
    generate_tests_for_folder(folder_path, test_dir)
    print(f"Test cases have been generated in: {test_dir}")

def generate_test_file(file_path, output_folder):
    component_name = os.path.splitext(os.path.basename(file_path))[0]
    test_dir = os.path.join(output_folder)
    generate_test_case(file_path, component_name, test_dir)
    print(f"Test case has been generated for: {file_path}")

def install_npm_dependencies(root_dir):
    dependencies = [
        "@babel/core",
        "@babel/preset-env",
        "@babel/preset-react",
        "babel-jest",
        "jest-transform-stub",
        "jest",
        "jest-environment-jsdom",
        "@testing-library/react",
    ]
    subprocess.run(
        ["C:\\Program Files\\nodejs\\npm.cmd", "install", "--save-dev"] + dependencies,
        cwd=root_dir,
        check=True,
    )

def configure_package_json(root_dir, output_folder):
    package_json_path = os.path.join(root_dir, "package.json")

    package_json = {
        "dependencies": {
            "@babel/parser": "^7.26.3",
            "@babel/traverse": "^7.26.4",
            "@testing-library/jest-dom": "^6.6.3",
            "chai": "^5.1.2",
            "esprima": "^4.0.1",
            "itertools": "^2.3.2"
        },
        "devDependencies": {
            "@babel/core": "^7.26.0",
            "@babel/preset-env": "^7.26.0",
            "@babel/preset-react": "^7.26.3",
            "@testing-library/react": "^16.1.0",
            "babel-jest": "^29.7.0",
            "jest": "^29.7.0",
            "jest-environment-jsdom": "^29.7.0",
            "jest-transform-stub": "^2.0.0",
            "mocha": "^11.0.1"
        },
        "scripts": {
            "test": "jest"
        },
        "jest": {
            "transform": {
                "^.+\\.(js|jsx|ts|tsx)$": "babel-jest",
                "^.+\\.css$": "jest-transform-stub"
            },
            "moduleFileExtensions": [
                "js",
                "jsx"
            ],
            "testEnvironment": "jest-environment-jsdom",
            "testMatch": [f"<rootDir>/{output_folder}/**/*.test.js"]  # This line includes the tests directory
        }
    }

    with open(package_json_path, "w") as f:
        json.dump(package_json, f, indent=2)

    print("Jest configuration and test script have been added to package.json.")

def create_babel_config(root_dir):
    babel_config = """
module.exports = {
    presets: ['@babel/preset-env', '@babel/preset-react'],
};
"""
    babel_config_path = os.path.join(root_dir, "babel.config.js")
    with open(babel_config_path, "w") as f:
        f.write(babel_config)
    print("babel.config.js has been created.")

def generate_and_run_test(path, output_folder):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if os.path.isdir(path):
        process_folder(path, output_folder)
    elif os.path.isfile(path) and path.endswith(".js"):
        generate_test_file(path, output_folder)
    else:
        print("Invalid path. Please provide a valid JavaScript file or folder.")

    # Install npm dependencies
    try:
        install_npm_dependencies(root_dir)
    except subprocess.CalledProcessError:
        print(
            "Error: npm dependencies could not be installed. Please ensure you have npm installed and try again."
        )
        exit(1)

    # Configure Jest in package.json
    configure_package_json(root_dir, output_folder)

    # Create babel.config.js
    create_babel_config(root_dir)

    # Run tests
    print("Running tests...")
    subprocess.run(["C:\\Program Files\\nodejs\\npm.cmd", "test"], cwd=root_dir)

if __name__ == "__main__":
    path = os.getenv("FOLDER_PATH")
    output_folder = os.getenv("OUTPUT_FOLDER")

    generate_and_run_test(path, output_folder)