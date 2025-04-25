import os
import cv2
import numpy as np
from skimage.feature import hog
import joblib

# Path to your single‐image SVM
MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 "..", "models", "svm_model.pkl")
)
svm_model = joblib.load(MODEL_PATH)

# Path to your pairwise SVM
PAIRWISE_MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__),
                 "..", "models", "svm_pairwise_model.pkl")
)
pairwise_svm = joblib.load(PAIRWISE_MODEL_PATH)


def preprocess_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {path}")
    img = cv2.resize(img, (128, 128))
    feats, _ = hog(
        img, orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm='L2-Hys',
        visualize=True,
        transform_sqrt=True
    )
    return feats


def predict_signature(image_path):
    """
    Classify a single test signature via the standalone SVM.
    """
    feats = preprocess_image(image_path).reshape(1, -1)
    pred = svm_model.predict(feats)[0]       # 0=genuine, 1=forged
    return "Genuine" if pred == 0 else "Forged"


def verify_signature_pairwise(original_path, test_path):
    """
    Compare an original & test via the pairwise‐trained SVM.
    Returns (label, prob_genuine).
    """
    f1 = preprocess_image(original_path)
    f2 = preprocess_image(test_path)
    diff = np.abs(f1 - f2).reshape(1, -1)

    pred = pairwise_svm.predict(diff)[0]            # 0=genuine, 1=forged
    prob = pairwise_svm.predict_proba(diff)[0][0]   # P(genuine)
    label = "Genuine" if pred == 0 else "Forged"
    return label, float(prob)
