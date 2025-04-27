import React from "react";
import SignatureUpload from "./components/SignatureUpload";
import SignatureVerify from "./components/SignatureVerify";

function App() {
  const headingStyle = {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
  };
  return (
    <div className="App">
      <h1 style={headingStyle}>Signature Forgery Detection</h1>
      <SignatureUpload />
      <SignatureVerify />
    </div>
  );
}

export default App;
