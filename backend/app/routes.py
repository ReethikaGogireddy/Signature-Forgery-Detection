import os
import base64
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.utils import predict_signature  # loads svm_model.pkl and does HOG + SVM
from app.utils import verify_signature  

main = Blueprint('main', __name__)

@main.route('/upload_originals', methods=['POST'])
def upload_originals():
    files = request.files.getlist('signatures')
    print(">>> Received files:", files)          # debug
    print(">>> request.files keys:", request.files.keys())

    if not files:
        return jsonify({'error': 'No files provided'}), 400

    save_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'originals')
    save_dir = os.path.abspath(save_dir)
    print(">>> Saving originals into:", save_dir)  # debug
    os.makedirs(save_dir, exist_ok=True)

    saved = []
    for f in files:
        print(">>> Processing file:", f.filename)  # debug
        if f and f.filename:
            filename = secure_filename(f.filename)
            path = os.path.join(save_dir, filename)
            f.save(path)
            saved.append(filename)

    print(f">>> Actually saved {len(saved)} files:", saved)  # debug
    return jsonify({
        'message': f'Saved {len(saved)} files.',
        'filenames': saved
    }), 200



@main.route('/upload_online', methods=['POST'])
def upload_online():
    data = request.get_json()
    if 'signature_data' not in data:
        return jsonify({'error': 'No signature data provided'}), 400

    # signature_data is a Base64 string like "data:image/png;base64,AAA..."
    header, encoded = data['signature_data'].split(",", 1)
    binary = base64.b64decode(encoded)

    # Save the file
    filename = secure_filename("online_signature.png")
    save_path = os.path.join('backend/data/originals', filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as f:
        f.write(binary)

    # Predict using your SVM model
    prediction = predict_signature(save_path)
    return jsonify({'prediction': prediction})




@main.route('/originals', methods=['GET'])
def list_originals():
    orig_dir = os.path.join(os.getcwd(), 'backend', 'data', 'originals')
    files = sorted(os.listdir(orig_dir)) if os.path.isdir(orig_dir) else []
    return jsonify({'originals': files}), 200

@main.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    orig_fn = data.get('original_filename')
    sig_data = data.get('signature_data')
    if not orig_fn or not sig_data:
        return jsonify({'error': 'Missing original_filename or signature_data'}), 400

    orig_path = os.path.join(os.getcwd(), 'backend', 'data', 'originals', orig_fn)
    if not os.path.isfile(orig_path):
        return jsonify({'error': f'Original {orig_fn} not found'}), 400

    # save test
    header, encoded = sig_data.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    test_dir = os.path.join(os.getcwd(), 'backend', 'data', 'tests')
    os.makedirs(test_dir, exist_ok=True)
    test_path = os.path.join(test_dir, f"test_{orig_fn}")
    with open(test_path, 'wb') as f:
        f.write(img_bytes)

    # verify
    result, score = verify_signature(orig_path, test_path)
    return jsonify({'result': result, 'score': score}), 200
