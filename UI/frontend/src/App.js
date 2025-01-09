import React, { useState } from 'react';
import './App.css';

function App() {
  const [folderPath, setFolderPath] = useState('');
  const [testResults, setTestResults] = useState(null);

  // Handle folder selection using file input
  const handleFolderSelect = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      const relativePath = files[0].webkitRelativePath || '';
      const selectedFolderPath = relativePath.split('/')[0]; // Extract the folder path
      setFolderPath(selectedFolderPath);
    }
  };

  const handleRunTests = async () => {
    if (!folderPath) {
      alert("Please select or enter a folder path before running tests.");
      return;
    }
  
    try {
      const response = await fetch("http://127.0.0.1:8000/save-folder", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ folderPath }),
      });
  
      if (!response.ok) {
        throw new Error("Failed to connect to the backend.");
      }
  
      const data = await response.json();
      console.log("Response from backend:", data);
  
      const mockResults = {
        passed: 4,
        failed: 1,
        details: [
          { status: "PASS", file: "src/tests/Form.test.js" },
          { status: "PASS", file: "src/tests/Utils.test.js" },
          { status: "FAIL", file: "src/tests/TodoList.test.js" },
        ],
      };
  
      setTestResults(mockResults); // Replace with actual test results from backend
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while running tests. Please try again.");
    }
  };
  

  const handleClear = () => {
    setFolderPath('');
    setTestResults(null);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>INTELLICO</h1>
      </header>

      <main className="main-container">
        <div className="content-box">
          {/* Folder Selection */}
          <div className="folder-section">
            <label>Select Folder</label>
            <div className="input-group">
              <input
                type="text"
                value={folderPath}
                onChange={(e) => setFolderPath(e.target.value)}
                placeholder="Enter folder path"
              />
              <button
                className="browse-btn"
                onClick={() =>
                  document.getElementById('folder-select').click()
                }
              >
                Browse
              </button>
              <input
                type="file"
                id="folder-select"
                webkitdirectory="true"
                onChange={handleFolderSelect}
                style={{ display: 'none' }}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="action-section">
            <button className="run-btn" onClick={handleRunTests}>
              Run Tests
            </button>
            <button className="clear-btn" onClick={handleClear}>
              Clear
            </button>
          </div>

          {/* Results or Welcome Message */}
          {!testResults ? (
            <div className="welcome-section">
              <h2>Welcome to Intellico</h2>
              <p className="start-text">To get started:</p>
              <ol>
                <li>
                  Enter a folder path or click 'Browse' to select a folder
                </li>
                <li>Click 'Run Tests' to begin automated testing</li>
              </ol>
              <p className="languages-text">
                Supported Languages: JavaScript (Jest) | Python (Pytest) | More...
              </p>
            </div>
          ) : (
            <div className="results-section">
              <h3>Test Results</h3>

              <div className="results-summary">
                <div className="result-count">
                  <span className="count pass">{testResults.passed}</span>
                  <span>Passed</span>
                </div>
                <div className="result-count">
                  <span className="count fail">{testResults.failed}</span>
                  <span>Failed</span>
                </div>
              </div>

              <div className="results-details">
                {testResults.details.map((result, index) => (
                  <div
                    key={index}
                    className={`result-item ${result.status.toLowerCase()}`}
                  >
                    {result.status === 'PASS' ? '✓' : '✗'} {result.status}{' '}
                    {result.file}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;












// import React, { useState } from "react";
// import axios from "axios"; // Import Axios
// import "./App.css";

// function App() {
//   const [folderPath, setFolderPath] = useState(""); // Store the folder path
//   const [message, setMessage] = useState(""); // Display messages to the user

//   // Handle changes in the text input for folder path
//   const handleFolderChange = (event) => {
//     setFolderPath(event.target.value); // Update the folder path state
//   };

//   // Handle folder selection using file input
//   const handleFolderSelect = (event) => {
//     const files = event.target.files;
//     console.log(files, 'files')

//     if (files.length > 0) {
//       // Extract the folder path from the first file's relative path
//       const relativePath = files[0].webkitRelativePath || "";
//       console.log(relativePath, 'relative path')
//       const folderPath = relativePath.split("/")[0]; // Get the root folder name
//       setFolderPath(folderPath); // Save the folder path
//       setMessage(`Folder path selected: ${folderPath}`);
//     } else {
//       setMessage("No folder selected. Please try again.");
//     }
//   };

//   // Handle submission of the folder path
//   const handleSubmit = async () => {
//     if (!folderPath) {
//       setMessage("Please enter or select a folder path."); // Error message if no path is set
//       return;
//     }

//     // Send the folder path to the FastAPI backend
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/save-folder", {
//         folderPath: folderPath, // Send the folder path in the request body
//       });

//       // Handle response
//       setMessage(response.data.message || `Folder path saved: ${folderPath}`);
//       console.log("Response from backend:", response.data); // For debugging purposes
//     } catch (error) {
//       console.error("Error sending folder path:", error);
//       setMessage("An error occurred while saving the folder path.");
//     }
//   };

//   return (
//     <div className="App">
//       <h1>Intellico</h1>

//       {/* Manual Text Input for Folder Path */}
//       <div className="folder-input">
//         <label htmlFor="folder-path">Enter Folder Path:</label>
//         <input
//           type="text"
//           id="folder-path"
//           value={folderPath}
//           onChange={handleFolderChange}
//           placeholder="Enter the folder path here"
//         />
//       </div>

//       {/* File Input to Select Folder */}
//       <div className="folder-input">
//         {/* The label "Or Select Folder" is no longer clickable */}
//         <span>Or Select Folder:</span>
//         <input
//           type="file"
//           id="folder-select"
//           webkitdirectory="true"
//           onChange={handleFolderSelect}
//           style={{ display: "none" }} // Hide the input field
//         />
//       </div>

//       {/* Button to trigger folder selection (use button to trigger the hidden file input) */}
//       <button
//         className="select-button"
//         onClick={() => document.getElementById("folder-select").click()}
//       >
//         Select Folder
//       </button>

//       {/* Submit Button */}
//       <button className="submit-button" onClick={handleSubmit}>
//         Save Folder Path
//       </button>

//       {/* Display Message */}
//       {message && <p className="message">{message}</p>}
//     </div>
//   );
// }

// export default App;







