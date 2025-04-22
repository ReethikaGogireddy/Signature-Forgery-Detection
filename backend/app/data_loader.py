import os
import cv2
import numpy as np
from skimage.feature import hog

def load_signature_dataset(base_dir):
    """
    Walk through base_dir/signatures_*/ folders, extract HOG features,
    and return X (features) and y (labels: 0=genuine, 1=forged).
    """
    X, y = [], []

    # Iterate over each signer-folder: signatures_1, signatures_2, …
    for signer_folder in sorted(os.listdir(base_dir)):
        signer_path = os.path.join(base_dir, signer_folder)
        if not os.path.isdir(signer_path):
            continue

        # Process each image file in that folder
        for fname in os.listdir(signer_path):
            if not fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                continue

            img_path = os.path.join(signer_path, fname)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"⚠️  Could not read {img_path}, skipping.")
                continue

            # Resize to a fixed size
            img = cv2.resize(img, (128, 128))

            # Extract HOG features
            features, _ = hog(
                img,
                orientations=9,
                pixels_per_cell=(8, 8),
                cells_per_block=(2, 2),
                block_norm='L2-Hys',
                visualize=True,
                transform_sqrt=True
            )
            X.append(features)

            # Determine label from filename prefix
            if fname.startswith("original_"):
                y.append(0)   # genuine
            elif fname.startswith("forgeries_"):
                y.append(1)   # forged
            else:
                print(f"⚠️  Unrecognized prefix in {fname}, skipping.")
    
    return np.array(X), np.array(y)


# Example usage:
if __name__ == "__main__":
    base = os.path.abspath(os.path.join(__file__, "..", "..", "signatures"))
    print("Loading dataset from:", base)
    X, y = load_signature_dataset(base)
    print(f"Loaded {len(y)} samples → Genuine: {(y==0).sum()}, Forged: {(y==1).sum()}")
