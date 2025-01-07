import os
from collections import Counter

# Middleware functions
def python_middleware(folder_path):
    print(f"Processing folder '{folder_path}' with Python middleware...")

def javascript_middleware(folder_path):
    print(f"Processing folder '{folder_path}' with JavaScript middleware...")

def java_middleware(folder_path):
    print(f"Processing folder '{folder_path}' with Java middleware...")

def unknown_middleware(folder_path):
    print(f"Processing folder '{folder_path}' with Unknown middleware...")

# Map languages to middleware
def call_middleware(language, folder_path):
    middleware_map = {
        'Python': python_middleware,
        'JavaScript': javascript_middleware,
        'Java': java_middleware,
        'Unknown': unknown_middleware,
    }
    middleware = middleware_map.get(language, unknown_middleware)
    middleware(folder_path)

# Identify the folder's dominant language
def predict_folder_language(file_language_counts):
    # Rule-based logic to predict folder language
    return file_language_counts.most_common(1)[0][0] if file_language_counts else 'Unknown'

# Main function
def analyze_folder(folder_path):
    if not os.path.isdir(folder_path):
        print(f"The provided path '{folder_path}' is not a valid directory.")
        return

    print(f"Analyzing directory: {folder_path}\n")

    for root, dirs, files in os.walk(folder_path):
        print(f"Current directory: {root}")
        file_language_counts = Counter()

        for file in files:
            file_extension = os.path.splitext(file)[1]
            if file_extension == '.py':
                file_language_counts['Python'] += 1
            elif file_extension == '.js':
                file_language_counts['JavaScript'] += 1
            elif file_extension == '.java':
                file_language_counts['Java'] += 1

        print(f"Relevant file counts in {root}: {dict(file_language_counts)}")

        # Predict folder language
        folder_language = predict_folder_language(file_language_counts)
        print(f"Predicted language for folder '{root}': {folder_language}\n")

        # Call middleware
        call_middleware(folder_language, root)

if __name__ == "__main__":
    folder_path = input("Enter the folder path to analyze: ").strip()
    analyze_folder(folder_path)
