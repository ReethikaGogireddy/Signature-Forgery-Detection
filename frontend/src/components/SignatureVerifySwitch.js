import React, { useEffect, useRef, useState } from "react";
import SignatureCanvas from "react-signature-canvas";

export default function SignatureVerifySwitch() {
  const API = process.env.REACT_APP_API_URL || "http://localhost:5000";
  const [originals, setOriginals] = useState([]);
  const [selected, setSelected] = useState("");
  const [model, setModel] = useState("svm");
  const [message, setMessage] = useState("");
  const sigCanvas = useRef(null);

  useEffect(() => {
    fetch(`${API}/originals`)
      .then((r) => r.json())
      .then((j) => j.originals && setOriginals(j.originals));
  }, [API]);

  const handleVerify = async () => {
    if (!selected) return setMessage("Select an original first.");
    if (sigCanvas.current.isEmpty()) return setMessage("Draw signature.");

    const res = await fetch(`${API}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        original_filename: selected,
        signature_data: sigCanvas.current.toDataURL(),
        model: model,
      }),
    });
    const j = await res.json();
    setMessage(
      res.ok
        ? `(${model.toUpperCase()}) ${j.result} (score: ${j.score.toFixed(2)})`
        : `Error: ${j.error}`
    );
  };

  // inline styles for brevity
  const selStyle = { padding: 8, margin: 8, fontSize: 16 },
    btnStyle = {
      padding: "10px 20px",
      margin: 8,
      background: "#007bff",
      color: "#fff",
      border: "none",
      borderRadius: 4,
    };

  return (
    <div style={{ textAlign: "center", padding: 20 }}>
      <h2>Choose Model & Original</h2>
      <select
        style={selStyle}
        value={model}
        onChange={(e) => setModel(e.target.value)}
      >
        <option value="svm">Pairwise SVM</option>
        <option value="rf">Random Forest</option>
        <option value="logistic">Logistic (Sigmoid)</option>
        <option value="cnn">Siamese-CNN</option>
      </select>
      <select
        style={selStyle}
        value={selected}
        onChange={(e) => setSelected(e.target.value)}
      >
        <option value="">-- pick original --</option>
        {originals.map((fn) => (
          <option key={fn}>{fn}</option>
        ))}
      </select>

      <h2>Draw Test Signature</h2>
      <div
        style={{
          border: "2px dashed #ccc",
          display: "inline-block",
          padding: 12,
          margin: 12,
        }}
      >
        <SignatureCanvas
          ref={sigCanvas}
          penColor="black"
          canvasProps={{ width: 400, height: 150, style: { borderRadius: 4 } }}
        />
      </div>
      <div>
        <button style={btnStyle} onClick={() => sigCanvas.current.clear()}>
          Clear
        </button>
        <button style={btnStyle} onClick={handleVerify}>
          Verify
        </button>
      </div>
      {message && <p style={{ marginTop: 20, fontSize: 18 }}>{message}</p>}
    </div>
  );
}
