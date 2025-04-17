import cv2
import numpy as np
from skimage.feature import hog
import joblib

# Load the SVM model (ensure svm_model.pkl is in the correct directory)
MODEL_PATH = 'backend/models/svm_model.pkl'
svm_model = joblib.load(MODEL_PATH)

def preprocess_image(image_path):
    # Load image in grayscale and resize for consistency
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (128, 128))
    # Extract HOG features
    features, _ = hog(image, orientations=9, pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2), block_norm='L2-Hys',
                      visualize=True, transform_sqrt=True)
    return features

def predict_signature(image_path):
    features = preprocess_image(image_path)
    features = features.reshape(1, -1)  # Format for the SVM
    pred = svm_model.predict(features)
    return 'Genuine' if pred[0] == 0 else 'Forged'
