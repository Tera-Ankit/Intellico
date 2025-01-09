import sys
import os

# from dotenv import load_dotenv

# load_dotenv()
# folder_name = os.getenv("FOLDER_NAME")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Python Path:", sys.path)
print("Current Working Directory:", os.getcwd())

from TestCase.testgenerator import generate_and_run_test
from sampletestcase.test_case_generator import TestCaseGenerator

from collections import Counter

# output_folder = os.getenv("OUTPUT_FOLDER", "tests")


# Middleware functions
def python_middleware(folder_path, output_folder):
    print(f"Processing folder '{folder_path}' with Python middleware...")
    # folder_name = os.path.basename(folder_path)
    generator = TestCaseGenerator(folder_path, output_folder)
    generator.run()


def javascript_middleware(folder_path, output_folder):
    print(f"Processing folder '{folder_path}' with JavaScript middleware...")
    # Identify JavaScript files in the folder
    generate_and_run_test(folder_path, output_folder)
    # for root, _, files in os.walk(folder_path):
    #     for file in files:
    #         if file.endswith(".js"):
    #             js_file_path = os.path.join(root, file)
    #             print(f"Found JavaScript file: {js_file_path}")
    #             # Generate tests for the JavaScript file
    #             generate_test_file(js_file_path, output_folder)


def jsx_middleware(folder_path, output_folder):
    print(f"Processing folder '{folder_path}' with JSX middleware...")
    # Identify JavaScript files in the folder
    generate_and_run_test(folder_path, output_folder)
    # for root, _, files in os.walk(folder_path):
    #     for file in files:
    #         if file.endswith(".jsx"):
    #             js_file_path = os.path.join(root, file)
    #             print(f"Found JSX file: {js_file_path}")
    #             # Generate tests for the JavaScript file
    #             generate_test_file(js_file_path, output_folder)


def unknown_middleware(folder_path, output_folder):
    print(f"Processing folder '{folder_path}' with Unknown middleware...")


# Map languages to middleware
def call_middleware(language, folder_path, output_folder):
    middleware_map = {
        "Python": python_middleware,
        "JavaScript": javascript_middleware,
        "JSX": jsx_middleware,
        "Unknown": unknown_middleware,
    }
    middleware = middleware_map.get(language, unknown_middleware)
    middleware(folder_path, output_folder)


# Identify the folder's dominant language
def predict_folder_language(file_language_counts):
    return (
        file_language_counts.most_common(1)[0][0] if file_language_counts else "Unknown"
    )


# Main function
def analyze_folder(folder_path, output_folder):
    if not os.path.isdir(folder_path):
        print(f"The provided path '{folder_path}' is not a valid directory.")
        return

    print(f"Analyzing directory: {folder_path}\n")

    for root, _, files in os.walk(folder_path):
        print(f"Current directory: {root}")
        file_language_counts = Counter()

        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension == ".py":
                file_language_counts["Python"] += 1
            elif file_extension == ".js":
                file_language_counts["JavaScript"] += 1
            elif file_extension == ".jsx":
                file_language_counts["JSX"] += 1

        print(f"Relevant file counts in {root}: {dict(file_language_counts)}")

        # Predict folder language
        folder_language = predict_folder_language(file_language_counts)
        print(f"Predicted language for folder '{root}': {folder_language}\n")

        # Call middleware
        call_middleware(folder_language, root, output_folder)


if __name__ == "__main__":
    folder_path = input("Enter the folder path to analyze: ").strip()
    output_folder = (
        input("Enter the output folder for test files (default: tests): ").strip()
        or "tests"
    )
    analyze_folder(folder_path, output_folder)
