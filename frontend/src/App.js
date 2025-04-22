import React from "react";
import SignatureCanvasComponent from "./components/SignatureCanvas";
import SignatureUpload from "./components/SignatureUpload";
import SignatureVerify from "./components/SignatureVerify";

function App() {
  return (
    <div className="App">
      <h1>Signature Forgery Detection</h1>
      <SignatureCanvasComponent />
      <SignatureUpload />
      <SignatureVerify />
    </div>
  );
}

export default App;
