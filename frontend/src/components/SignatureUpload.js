import React, { useState } from "react";

export default function SignatureUpload() {
  const [files, setFiles] = useState([]);
  const [response, setResponse] = useState(null);
  const API = process.env.REACT_APP_API_URL || "http://localhost:5000";

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setResponse(null);
  };

  const uploadAll = async () => {
    if (files.length === 0) {
      alert("Please select at least one file.");
      return;
    }
    const formData = new FormData();
    files.forEach((file) => formData.append("signatures", file));

    try {
      const res = await fetch(`${API}/upload_originals`, {
        method: "POST",
        body: formData,
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || "Upload failed");
      setResponse(json);
    } catch (err) {
      setResponse({ error: err.message });
    }
  };

  // Inline style objects
  const containerStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "60vh",
    backgroundColor: "#f9f9f9",
    padding: 20,
  };
  const headingStyle = {
    fontSize: 24,
    color: "#333",
    marginBottom: 16,
  };
  const inputStyle = {
    marginBottom: 12,
  };
  const buttonStyle = {
    padding: "10px 20px",
    fontSize: 16,
    border: "none",
    borderRadius: 4,
    backgroundColor: "#007bff",
    color: "#fff",
    cursor: "pointer",
  };
  const responseContainerStyle = {
    marginTop: 20,
    textAlign: "center",
  };
  const errorTextStyle = {
    color: "red",
    fontWeight: "bold",
  };
  const listStyle = {
    listStyleType: "none",
    paddingLeft: 0,
    marginTop: 8,
  };
  const listItemStyle = {
    margin: "4px 0",
    color: "#555",
  };

  return (
    <div style={containerStyle}>
      <h2 style={headingStyle}>Upload Original Signatures</h2>

      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleFileChange}
        style={inputStyle}
      />

      <button onClick={uploadAll} style={buttonStyle}>
        Upload All
      </button>

      {response && (
        <div style={responseContainerStyle}>
          {response.error ? (
            <p style={errorTextStyle}>Error: {response.error}</p>
          ) : (
            <>
              <p>{response.message}</p>
              <ul style={listStyle}>
                {response.filenames.map((fn) => (
                  <li key={fn} style={listItemStyle}>
                    {fn}
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
