import os
import json
import subprocess


def generate_test_case(component_path, component_name, test_dir):
    component_dir = os.path.dirname(component_path)
    relative_path = os.path.relpath(component_dir, test_dir).replace(os.sep, '/')

    import_statement = f"import {{ {component_name} }} from '{relative_path}/{component_name}';"

    try:
        with open(component_path, 'r') as f:
            content = f.read()
            if 'export default' in content:
                import_statement = f"import {component_name} from '{relative_path}/{component_name}';"
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
    with open(test_file_path, 'w') as f:
        f.write(test_content)


def generate_tests_for_folder(folder_path, test_dir):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.js') or file.endswith('.jsx'):
                component_path = os.path.join(root, file)
                component_name = os.path.splitext(file)[0]
                generate_test_case(component_path, component_name, test_dir)


def process_folder(folder_path, output_folder):
    test_dir = os.path.join(folder_path, output_folder)
    generate_tests_for_folder(folder_path, test_dir)
    print(f"Test cases have been generated in: {test_dir}")


def generate_test_file(file_path, output_folder):
    component_name = os.path.splitext(os.path.basename(file_path))[0]
    test_dir = os.path.join(os.path.dirname(file_path), output_folder)
    generate_test_case(file_path, component_name, test_dir)
    print(f"Test case has been generated for: {file_path}")


def install_npm_dependencies():
    dependencies = [
        "@babel/core",
        "@babel/preset-env",
        "@babel/preset-react",
        "babel-jest",
        "jest-transform-stub",
        "jest",
        "jest-environment-jsdom",
        "@testing-library/react"
    ]
    # print("Installing npm dependencies...")
    subprocess.run(["C:\\Program Files\\nodejs\\npm.cmd", "install", "--save-dev"] + dependencies, check=True)
    # print("npm dependencies installed successfully.")


def configure_package_json():
    package_json_path = "package.json"

    if not os.path.exists(package_json_path):
        print("Error: No package.json found in the current directory.")
        return

    with open(package_json_path, 'r') as f:
        package_json = json.load(f)

    package_json['jest'] = {
        "transform": {
            "^.+\\.(js|jsx|ts|tsx)$": "babel-jest",
            "^.+\\.css$": "jest-transform-stub"
        },
        "moduleFileExtensions": ["js", "jsx"],
        "testEnvironment": "jest-environment-jsdom"
    }

    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=2)

    print("Jest configuration has been added to package.json.")


def create_babel_config():
    babel_config = """
module.exports = {
    presets: ['@babel/preset-env', '@babel/preset-react'],
};
"""
    with open("babel.config.js", 'w') as f:
        f.write(babel_config)
    print("babel.config.js has been created.")


if __name__ == "__main__":
    path = input("Enter the path to the JavaScript file or folder: ").strip()
    output_folder = "tests"

    if os.path.isdir(path):
        process_folder(path, output_folder)
    elif os.path.isfile(path) and path.endswith(".js"):
        generate_test_file(path, output_folder)
    else:
        print("Invalid path. Please provide a valid JavaScript file or folder.")

    # Install npm dependencies
    try:
        install_npm_dependencies()
    except subprocess.CalledProcessError:
        print("Error: npm dependencies could not be installed. Please ensure you have npm installed and try again.")
        exit(1)

    # Configure Jest in package.json
    configure_package_json()

    # Create babel.config.js
    create_babel_config()

    # Run tests
    print("Running tests...")
    subprocess.run(["C:\\Program Files\\nodejs\\npm.cmd", "test"])
