import React, { useState } from "react";
import axios from "axios"; // Import Axios
import "./App.css";

function App() {
  const [folderPath, setFolderPath] = useState(""); // Store the folder path
  const [message, setMessage] = useState(""); // Display messages to the user

  // Handle changes in the text input for folder path
  const handleFolderChange = (event) => {
    setFolderPath(event.target.value); // Update the folder path state
  };

  // Handle folder selection using file input
  const handleFolderSelect = (event) => {
    const files = event.target.files;
    console.log(files, 'files')

    if (files.length > 0) {
      // Extract the folder path from the first file's relative path
      const relativePath = files[0].webkitRelativePath || "";
      console.log(relativePath, 'relative path')
      const folderPath = relativePath.split("/")[0]; // Get the root folder name
      setFolderPath(folderPath); // Save the folder path
      setMessage(`Folder path selected: ${folderPath}`);
    } else {
      setMessage("No folder selected. Please try again.");
    }
  };

  // Handle submission of the folder path
  const handleSubmit = async () => {
    if (!folderPath) {
      setMessage("Please enter or select a folder path."); // Error message if no path is set
      return;
    }

    // Send the folder path to the FastAPI backend
    try {
      const response = await axios.post("http://localhost:8000/save-folder", {
        folderPath: folderPath, // Send the folder path in the request body
      });

      // Handle response
      setMessage(response.data.message || `Folder path saved: ${folderPath}`);
      console.log("Response from backend:", response.data); // For debugging purposes
    } catch (error) {
      console.error("Error sending folder path:", error);
      setMessage("An error occurred while saving the folder path.");
    }
  };

  return (
    <div className="App">
      <h1>Intellico</h1>

      {/* Manual Text Input for Folder Path */}
      <div className="folder-input">
        <label htmlFor="folder-path">Enter Folder Path:</label>
        <input
          type="text"
          id="folder-path"
          value={folderPath}
          onChange={handleFolderChange}
          placeholder="Enter the folder path here"
        />
      </div>

      {/* File Input to Select Folder */}
      <div className="folder-input">
        {/* The label "Or Select Folder" is no longer clickable */}
        <span>Or Select Folder:</span>
        <input
          type="file"
          id="folder-select"
          webkitdirectory="true"
          onChange={handleFolderSelect}
          style={{ display: "none" }} // Hide the input field
        />
      </div>

      {/* Button to trigger folder selection (use button to trigger the hidden file input) */}
      <button
        className="select-button"
        onClick={() => document.getElementById("folder-select").click()}
      >
        Select Folder
      </button>

      {/* Submit Button */}
      <button className="submit-button" onClick={handleSubmit}>
        Save Folder Path
      </button>

      {/* Display Message */}
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;







