from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins for CORS (you can restrict this to specific domains in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains to access your backend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class FolderPathRequest(BaseModel):
    folderPath: str

@app.post("/save-folder")
async def save_folder_path(request: FolderPathRequest):
    folder_path = request.folderPath
    print(f"Folder path received: {folder_path}")  # This will print the folder path to the terminal
    return {"message": f"Folder path '{folder_path}' saved successfully!"}
