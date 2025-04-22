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
    // Convert signature to Base64 string
    const dataURL = sigCanvas.current.toDataURL();

    try {
      const res = await fetch(`${API_URL}/upload_online`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ signature_data: dataURL }),
      });
      const data = await res.json();
      if (data.error) {
        setResult(`Error: ${data.error}`);
      } else {
        setResult(`Prediction: ${data.prediction}`);
      }
    } catch (error) {
      console.error("Upload error:", error);
      setResult("Upload failed. Please try again.");
    }
  };

  return (
    <div>
      <h2>Online Signature Capture</h2>
      <SignatureCanvas
        ref={sigCanvas}
        penColor="black"
        canvasProps={{ width: 500, height: 200, className: "sigCanvas" }}
      />
      <div style={{ marginTop: 10 }}>
        <button onClick={clearSignature}>Clear</button>
        <button onClick={saveSignature} style={{ marginLeft: 8 }}>
          Submit
        </button>
      </div>
      {result && (
        <div style={{ marginTop: 16 }}>
          <strong>{result}</strong>
        </div>
      )}
    </div>
  );
};

export default SignatureCanvasComponent;
