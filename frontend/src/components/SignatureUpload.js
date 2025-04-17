import React, { useState } from "react";

const SignatureUpload = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadSignature = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("signature", file);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data.prediction);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h2>Upload Signature</h2>
      <form onSubmit={uploadSignature}>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          required
        />
        <button type="submit">Upload</button>
      </form>
      {result && <h3>Prediction: {result}</h3>}
    </div>
  );
};

export default SignatureUpload;
