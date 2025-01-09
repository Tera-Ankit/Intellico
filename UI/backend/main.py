
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# from TestCase.testgenerator import generate_test_file
from language_identifier.main import analyze_folder

app = FastAPI()

# Allow all origins for CORS (you can restrict this to specific domains in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains to access your backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# output_folder = os.getenv("OUTPUT_FOLDER")


class FolderPathRequest(BaseModel):
    folderPath: str

output_folder=os.getenv("OUTPUT_FOLDER")
print(f"Output folder: {output_folder}")

@app.post("/save-folder")
async def save_folder_path(request: FolderPathRequest):
    folder_path = request.folderPath
    print(
        f"Folder path received: {folder_path}"
    )  # This will print the folder path to the terminal
    analyze_folder(folder_path, output_folder)
    # generate_test_file(folder_path)
    print(f"Test case has been generated for: {folder_path}")
    return {"message": f"Folder path '{folder_path}' saved successfully!"}
