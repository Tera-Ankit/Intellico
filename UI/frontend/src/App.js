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
    setFolderPath('');
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
                Supported Languages: JavaScript | Python | More...
              </p>
            </div>
          ) : (
            <div className="results-section">
              <h3>Test Results</h3>

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











