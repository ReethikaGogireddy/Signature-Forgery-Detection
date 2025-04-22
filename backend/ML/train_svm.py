# backend/ml/train_svm.py

import os
import cv2
import numpy as np
from skimage.feature import hog
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def extract_hog_features(image):
    """
    Resize grayscale image to 128×128 and extract HOG features.
    """
    image = cv2.resize(image, (128, 128))
    features, _ = hog(
        image,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm='L2-Hys',
        visualize=True,
        transform_sqrt=True
    )
    return features

def load_signature_dataset(base_dir):
    """
    Walks through base_dir/signatures_* folders, loads images prefixed
    original_ (genuine) or forgeries_ (forged), and returns (X, y).
    """
    X, y = [], []

    # List your signer subfolders: signatures_1, signatures_2, …
    signer_folders = sorted([
        d for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d))
    ])
    print("Found signer folders:", signer_folders)

    for folder in signer_folders:
        folder_path = os.path.join(base_dir, folder)
        for fname in os.listdir(folder_path):
            if not fname.lower().endswith(('.png','.jpg','.jpeg','.bmp')):
                continue

            img_path = os.path.join(folder_path, fname)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"⚠️  Failed to read {img_path}")
                continue

            feats = extract_hog_features(img)
            X.append(feats)

            if fname.startswith("original_"):
                y.append(0)
            elif fname.startswith("forgeries_"):
                y.append(1)
            else:
                # Unexpected prefix
                print(f"⚠️  Skipping unrecognized file: {fname}")

    X = np.array(X)
    y = np.array(y)

    # Sanity checks
    print(f"Total samples loaded: {len(y)}")
    if len(y)>0:
        print(f"HOG feature length: {X.shape[1]}")
        binc = np.bincount(y)
        print(f"Genuine(0): {binc[0] if len(binc)>0 else 0}, Forged(1): {binc[1] if len(binc)>1 else 0}")
    else:
        raise RuntimeError("No images loaded – check your 'signatures/' folder structure.")

    return X, y

def train_and_save():
    # Compute the path to the 'signatures' folder at project root
    script_dir     = os.path.dirname(__file__)            # .../backend/ml
    backend_dir    = os.path.abspath(os.path.join(script_dir, ".."))  # .../backend
    signatures_dir = os.path.join(backend_dir, "signatures")
    print("Loading data from:", signatures_dir)

    X, y = load_signature_dataset(signatures_dir)

    # Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train a linear-kernel SVM
    clf = svm.SVC(kernel='linear', probability=True)
    print("Training SVM...")
    clf.fit(X_train, y_train)

    # Evaluate on test set
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Test Accuracy: {acc*100:.2f}%")

    # Ensure `backend/models/` exists and save the model there
    model_dir = os.path.join( backend_dir, 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'svm_model.pkl')
    joblib.dump(clf, model_path)
    print("Model saved to:", model_path)

if __name__ == "__main__":
    train_and_save()
