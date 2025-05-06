# Signature Forgery Detection Web App

A simple web app to upload genuine signatures, draw a test signature, and verify it using a trained SVM model.



## Overview

1. **Upload Genuine Signatures**: Send one or more images to the server.
2. **Select a Signature**: Pick one of the saved originals.
3. **Draw Test Signature**: Sign on the canvas in the browser.
4. **Verify**: The app returns “Genuine” or “Forged” with a confidence score.


## Tech Stack

- **Backend**: Flask (Python), scikit-learn, OpenCV, joblib
- **Frontend**: React, react-signature-canvas



## Setup

1. **Backend**

   ```bash
   cd backend
   pip install -r requirements.txt
   python ml/train_svm.py   # trains and saves svm_model.pkl
   python run.py            # starts Flask on http://localhost:5000
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm start                # opens http://localhost:3000
   ```



## Usage

1. **Upload** genuine signatures via the frontend form.
2. **Select** an original from the dropdown.
3. **Draw** a new signature on the canvas.
4. **Verify** to see if it’s Genuine or Forged.



## File Locations

- **Genuine uploads**: `backend/data/originals/`
- **Test signatures**: `backend/data/tests/`
- **Model file**: `backend/models/svm_model.pkl`


