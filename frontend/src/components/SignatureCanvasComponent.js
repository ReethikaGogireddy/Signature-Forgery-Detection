import React, { useRef, useState } from "react";
import SignatureCanvas from "react-signature-canvas";

const SignatureCanvasComponent = () => {
  const sigCanvas = useRef(null);
  const [result, setResult] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

  const clearSignature = () => {
    sigCanvas.current.clear();
    setResult(null);
  };

  const saveSignature = async () => {
    if (sigCanvas.current.isEmpty()) {
      alert("Please provide a signature first.");
      return;
    }
    const dataURL = sigCanvas.current.toDataURL();
    try {
      const res = await fetch(`${API_URL}/upload_online`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ signature_data: dataURL }),
      });
      const data = await res.json();
      setResult(
        data.error ? `Error: ${data.error}` : `Prediction: ${data.prediction}`
      );
    } catch {
      setResult("Upload failed. Please try again.");
    }
  };

  // Inline style objects
  const containerStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#f0f0f0",
    padding: 20,
  };
  const headingStyle = { marginBottom: 24, fontSize: 28, color: "#333" };
  const canvasWrapperStyle = {
    border: "2px dashed #ccc",
    borderRadius: 8,
    backgroundColor: "#fff",
    padding: 16,
  };
  const canvasStyle = { borderRadius: 4, backgroundColor: "#fff" };
  const buttonsContainerStyle = { display: "flex", gap: 12, marginTop: 16 };
  const buttonStyle = {
    padding: "10px 20px",
    fontSize: 16,
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
    backgroundColor: "#007bff",
    color: "#fff",
  };
  const resultStyle = { marginTop: 20, fontSize: 18, color: "#333" };

  return (
    <div style={containerStyle}>
      <h2 style={headingStyle}>Online Signature Capture</h2>

      <div style={canvasWrapperStyle}>
        <SignatureCanvas
          ref={sigCanvas}
          penColor="black"
          canvasProps={{ width: 500, height: 200, style: canvasStyle }}
        />
      </div>

      <div style={buttonsContainerStyle}>
        <button style={buttonStyle} onClick={clearSignature}>
          Clear
        </button>
        <button style={buttonStyle} onClick={saveSignature}>
          Submit
        </button>
      </div>

      {result && (
        <div style={resultStyle}>
          <strong>{result}</strong>
        </div>
      )}
    </div>
  );
};

export default SignatureCanvasComponent;
