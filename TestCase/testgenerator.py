import os

def generate_test_case(component_path, component_name, test_dir):
    # Calculate the relative path from the component file to the 'tests' folder
    component_dir = os.path.dirname(component_path)
    relative_path = os.path.relpath(component_dir, test_dir)

    # Replace backslashes with forward slashes to ensure consistent path format
    relative_path = relative_path.replace(os.sep, '/')

    # Create the test case content
    test_content = f"""
const {component_name} = require('{relative_path}/{component_name}'); // Adjust path as necessary

describe('{component_name}', () => {{
  it('renders correctly', () => {{
    expect({component_name}).toBeDefined();
  }});
}});
    """

    # Ensure the test directory exists, then write the test case
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    test_file_path = os.path.join(test_dir, f"{component_name}.test.js")
    with open(test_file_path, 'w') as f:
        f.write(test_content)

def generate_tests_for_folder(folder_path, test_dir):
    # Walk through the folder and find all .js and .jsx files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.js') or file.endswith('.jsx'):
                # Get the full path of the component
                component_path = os.path.join(root, file)

                # Get the component name (file name without extension)
                component_name = os.path.splitext(file)[0]

                # Generate the test case
                generate_test_case(component_path, component_name, test_dir)

def process_folder(folder_path, output_folder):
    # Create the 'tests' folder
    test_dir = os.path.join(folder_path, output_folder)
    
    generate_tests_for_folder(folder_path, test_dir)
    print(f"Test cases have been generated in: {test_dir}")

def generate_test_file(file_path, output_folder):
    component_name = os.path.splitext(os.path.basename(file_path))[0]
    test_dir = os.path.join(os.path.dirname(file_path), output_folder)
    
    generate_test_case(file_path, component_name, test_dir)
    print(f"Test case has been generated for: {file_path}")

if __name__ == "__main__":
    # Get the path to the JavaScript file or folder and output folder from the user
    path = input("Enter the path to the JavaScript file or folder: ").strip()
    output_folder = input("Enter the output folder for test files (default: tests): ").strip() or "tests"

    if os.path.isdir(path):
        process_folder(path, output_folder)
    elif os.path.isfile(path) and path.endswith(".js"):
        generate_test_file(path, output_folder)
    else:
        print("Invalid path. Please provide a valid JavaScript file or folder.")
