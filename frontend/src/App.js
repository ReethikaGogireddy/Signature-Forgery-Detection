import React from "react";
import SignatureUpload from "./components/SignatureUpload";
//import SignatureVerify from "./components/SignatureVerify";
import SignatureVerifySwitch from "./components/SignatureVerifySwitch";

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
      <SignatureVerifySwitch />
    </div>
  );
}

export default App;
// function App() {
//   return (
//     <div>
//       <SignatureUpload />
//       <SignatureVerifySwitch />
//     </div>
//   );
// }
// export default App;
