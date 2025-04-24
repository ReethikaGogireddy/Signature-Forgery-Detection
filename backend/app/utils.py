# backend/app/utils.py
import os
import cv2
import numpy as np
from skimage.feature import hog
import joblib
from skimage.metrics import structural_similarity as ssim


# Build an absolute path to models/svm_model.pkl
MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),  # backend/app
        "..",                        # backend/
        "models",                    # backend/models
        "svm_model.pkl"
    )
)

# Now load it
svm_model = joblib.load(MODEL_PATH)

def preprocess_image(image_path):
    """
    Load an image from disk, convert to grayscale, resize, and extract HOG features.

    Parameters:
      image_path (str): Path to the image file.

    Returns:
      features (np.ndarray): 1D array of HOG features.
    """
    # 1. Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")

    # 2. Resize to 128×128 for consistency
    image = cv2.resize(image, (128, 128))

    # 3. Extract HOG features
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

def predict_signature(image_path):
    feats = preprocess_image(image_path).reshape(1, -1)
    pred = svm_model.predict(feats)
    return "Genuine" if pred[0] == 0 else "Forged"

def verify_signature(original_path, test_path):
    """
    Classify the test signature using the pre‐trained SVM.
    Returns label and the genuine‐class probability as score.
    """
    # We ignore original_path here, since the SVM is a standalone classifier.
    # 1. Extract HOG features from test image:
    feats = preprocess_image(test_path).reshape(1, -1)

    # 2. Get probabilities [P(genuine), P(forged)]
    probs = svm_model.predict_proba(feats)[0]
    prob_genuine = probs[0]

    # 3. Decide based on 0.5 threshold (or tune this)
    label = "Genuine" if prob_genuine >= 0.5 else "Forged"
    return label, float(prob_genuine)
