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

  return (
    <div>
      <h2>Upload Original Signatures</h2>
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleFileChange}
      />
      <button onClick={uploadAll} style={{ marginLeft: 8 }}>
        Upload All
      </button>

      {response && (
        <div style={{ marginTop: 16 }}>
          {response.error ? (
            <p style={{ color: "red" }}>Error: {response.error}</p>
          ) : (
            <>
              <p>{response.message}</p>
              <ul>
                {response.filenames.map((fn) => (
                  <li key={fn}>{fn}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}
