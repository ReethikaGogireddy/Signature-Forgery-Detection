import React from "react";
import SignatureUpload from "./components/SignatureUpload";
import SignatureVerify from "./components/SignatureVerify";

function App() {
  return (
    <div className="App">
      <h1>Signature Forgery Detection</h1>
      <SignatureUpload />
      <SignatureVerify />
    </div>
  );
}

export default App;
