import React, { useEffect, useRef, useState } from "react";
import SignatureCanvas from "react-signature-canvas";

export default function SignatureVerify() {
  const API = process.env.REACT_APP_API_URL || "http://localhost:5000";
  const [originals, setOriginals] = useState([]);
  const [selected, setSelected] = useState("");
  const [message, setMessage] = useState("");
  const sigCanvas = useRef(null);

  useEffect(() => {
    fetch(`${API}/originals`)
      .then((res) => res.json())
      .then((json) => {
        if (json.originals) setOriginals(json.originals);
      })
      .catch(console.error);
  }, [API]);

  const handleVerify = async () => {
    if (!selected) return setMessage("Select an original first.");
    if (sigCanvas.current.isEmpty()) return setMessage("Draw your signature.");

    const dataURL = sigCanvas.current.toDataURL();
    const res = await fetch(`${API}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        original_filename: selected,
        signature_data: dataURL,
      }),
    });
    const json = await res.json();
    if (!res.ok) return setMessage(`Error: ${json.error}`);
    setMessage(`Result: ${json.result} (score: ${json.score.toFixed(2)})`);
  };

  // Inline styles
  const container = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    minHeight: "100vh",
    backgroundColor: "#f0f0f0",
    padding: 20,
  };
  const heading = {
    fontSize: 24,
    color: "#333",
    margin: "8px 0",
  };
  const selectStyle = {
    width: 260,
    padding: 8,
    fontSize: 16,
    border: "2px solid #ccc",
    borderRadius: 4,
    backgroundColor: "#fff",
    marginBottom: 24,
  };
  const canvasWrapper = {
    border: "2px dashed #ccc",
    borderRadius: 8,
    backgroundColor: "#fff",
    padding: 12,
    marginBottom: 16,
  };
  const canvasStyle = {
    borderRadius: 4,
    backgroundColor: "#fff",
  };
  const buttons = {
    display: "flex",
    gap: 12,
    marginTop: 10,
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
  const messageStyle = {
    marginTop: 24,
    fontSize: 18,
    color: "#333",
    textAlign: "center",
  };

  return (
    <div style={container}>
      <h2 style={heading}>1. Select Original</h2>
      <select
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
        style={selectStyle}
      >
        <option value="">-- pick one --</option>
        {originals.map((fn) => (
          <option key={fn} value={fn}>
            {fn}
          </option>
        ))}
      </select>

      <h2 style={heading}>2. Draw Test Signature</h2>
      <div style={canvasWrapper}>
        <SignatureCanvas
          ref={sigCanvas}
          penColor="black"
          canvasProps={{
            width: 400,
            height: 150,
            style: canvasStyle,
          }}
        />
      </div>

      <div style={buttons}>
        <button
          style={buttonStyle}
          onClick={() => {
            sigCanvas.current.clear();
            setMessage("");
          }}
        >
          Clear
        </button>
        <button style={buttonStyle} onClick={handleVerify}>
          Verify
        </button>
      </div>

      {message && <div style={messageStyle}>{message}</div>}
    </div>
  );
}
