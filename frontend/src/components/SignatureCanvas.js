import React, { useRef } from "react";
import SignatureCanvas from "react-signature-canvas";

const SignatureCanvasComponent = () => {
  const sigCanvas = useRef({});

  const clearSignature = () => {
    sigCanvas.current.clear();
  };

  const saveSignature = () => {
    if (sigCanvas.current.isEmpty()) {
      alert("Please provide a signature first.");
      return;
    }
    // Convert signature to Base64 string
    const dataURL = sigCanvas.current.toDataURL();
    // Send the Base64 signature to the backend
    fetch("http://localhost:5000/upload_online", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ signature_data: dataURL }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("Signature processed: " + data.result);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <div>
      <h2>Online Signature Capture</h2>
      <SignatureCanvas
        ref={sigCanvas}
        penColor="black"
        canvasProps={{ width: 500, height: 200, className: "sigCanvas" }}
      />
      <br />
      <button onClick={clearSignature}>Clear</button>
      <button onClick={saveSignature}>Save Signature</button>
    </div>
  );
};

export default SignatureCanvasComponent;
