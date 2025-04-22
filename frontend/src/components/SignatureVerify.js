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

  return (
    <div>
      <h2>1. Select Original</h2>
      <select value={selected} onChange={(e) => setSelected(e.target.value)}>
        <option value="">-- pick one --</option>
        {originals.map((fn) => (
          <option key={fn} value={fn}>
            {fn}
          </option>
        ))}
      </select>

      <h2>2. Draw Test Signature</h2>
      <SignatureCanvas
        ref={sigCanvas}
        penColor="black"
        canvasProps={{
          width: 400,
          height: 150,
          style: { border: "1px solid #000" },
        }}
      />
      <div style={{ marginTop: 10 }}>
        <button
          onClick={() => {
            sigCanvas.current.clear();
            setMessage("");
          }}
        >
          Clear
        </button>
        <button onClick={handleVerify} style={{ marginLeft: 8 }}>
          Verify
        </button>
      </div>

      {message && <div style={{ marginTop: 20 }}>{message}</div>}
    </div>
  );
}
