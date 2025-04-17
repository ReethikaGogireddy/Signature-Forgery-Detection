import os
import cv2
import numpy as np
from skimage.feature import hog
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def extract_features(image_path):
    """
    Load an image, preprocess it, and extract HOG features.
    
    Parameters:
      image_path (str): Path to the image file.
    
    Returns:
      features (ndarray): 1D numpy array of HOG features.
    """
    # Load image in grayscale mode
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    # Resize image to a fixed size (128 x 128 pixels)
    image = cv2.resize(image, (128, 128))
    
    # Extract HOG features
    features, _ = hog(image, 
                      orientations=9, 
                      pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2), 
                      block_norm='L2-Hys',
                      visualize=True, 
                      transform_sqrt=True)
    return features

def load_dataset(genuine_dir, forged_dir):
    """
    Load the dataset from genuine and forged directories and extract features.
    
    Parameters:
      genuine_dir (str): Directory containing genuine signature images.
      forged_dir  (str): Directory containing forged signature images.
      
    Returns:
      X (ndarray): Array of feature vectors.
      y (ndarray): Array of labels (0 for genuine, 1 for forged).
    """
    features = []
    labels = []

    # Process genuine signatures (label as 0)
    for filename in os.listdir(genuine_dir):
        file_path = os.path.join(genuine_dir, filename)
        try:
            feat = extract_features(file_path)
            features.append(feat)
            labels.append(0)  # Genuine
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Process forged signatures (label as 1)
    for filename in os.listdir(forged_dir):
        file_path = os.path.join(forged_dir, filename)
        try:
            feat = extract_features(file_path)
            features.append(feat)
            labels.append(1)  # Forged
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return np.array(features), np.array(labels)

def train_and_save_model():
    """
    Train an SVM model on the provided signature dataset and save the trained model.
    """
    # Directories where the images are stored
    genuine_dir = 'data/genuine'
    forged_dir  = 'data/forged'
    
    print("Loading dataset and extracting features...")
    X, y = load_dataset(genuine_dir, forged_dir)

    print("Splitting dataset into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training the SVM classifier...")
    # Create an SVM classifier with a linear kernel; probability=True enables probability estimates.
    clf = svm.SVC(kernel='linear', probability=True)
    clf.fit(X_train, y_train)

    # Evaluate the classifier on the test set
    preds = clf.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    print("Accuracy on test data: {:.2f}%".format(accuracy * 100))

    # Save the trained model as svm_model.pkl
    model_path = 'svm_model.pkl'
    joblib.dump(clf, model_path)
    print(f"Trained model saved to {model_path}")

if __name__ == "__main__":
    train_and_save_model()
