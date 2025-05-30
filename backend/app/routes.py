import os, base64
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.utils import (
    predict_signature,
    verify_signature_pairwise,
    verify_rf,
    verify_logistic,
    verify_cnn
)

main = Blueprint('main', __name__)

@main.route('/upload_originals', methods=['POST']) #file uploading using flask
def upload_originals():
    files = request.files.getlist('signatures')
    if not files:
        return jsonify({'error': 'No files provided'}), 400

    save_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'originals')
    )
    os.makedirs(save_dir, exist_ok=True)

    saved = []
    for f in files:
        if f and f.filename:
            fn = secure_filename(f.filename)
            f.save(os.path.join(save_dir, fn))
            saved.append(fn)

    return jsonify({'message': f'Saved {len(saved)} files.', 'filenames': saved}), 200

@main.route('/upload_online', methods=['POST']) #signature drawing 
def upload_online():
    data = request.get_json() or {}
    img_b64 = data.get('signature_data')
    if not img_b64:
        return jsonify({'error': 'No signature data provided'}), 400

    # Save test signature
    header, encoded = img_b64.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    test_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tests')
    )
    os.makedirs(test_dir, exist_ok=True)
    test_path = os.path.join(test_dir, 'online_signature.png')
    with open(test_path, 'wb') as fp:
        fp.write(img_bytes)

    # Classify standalone
    prediction = predict_signature(test_path)
    return jsonify({'prediction': prediction}), 200

@main.route('/originals', methods=['GET'])
def list_originals():
    orig_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'originals')
    )
    files = sorted(os.listdir(orig_dir)) if os.path.isdir(orig_dir) else []
    return jsonify({'originals': files}), 200

@main.route('/verify', methods=['POST'])
def verify():
    data = request.get_json() or {}
    orig_fn = data.get('original_filename')
    img_b64 = data.get('signature_data')
    if not orig_fn or not img_b64:
        return jsonify({'error': 'Missing original_filename or signature_data'}), 400

    orig_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'originals')
    )
    orig_path = os.path.join(orig_dir, orig_fn)
    if not os.path.isfile(orig_path):
        return jsonify({'error': f'Original {orig_fn} not found'}), 400

    # Save test signature
    header, encoded = img_b64.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    test_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'tests')
    )
    os.makedirs(test_dir, exist_ok=True)
    test_path = os.path.join(test_dir, f'test_{orig_fn}')
    with open(test_path, 'wb') as fp:
        fp.write(img_bytes)

    # Pairwise verify
    #label, score = verify_signature_pairwise(orig_path, test_path)
    model = data.get('model', 'svm')  # 'svm', 'rf', 'logistic', 'cnn'
    if model == 'rf':
       result, score = verify_rf(orig_path, test_path)
    elif model == 'logistic':
       result, score = verify_logistic(orig_path, test_path)
    elif model == 'cnn':
       result, score = verify_cnn(orig_path, test_path)
    else:
       result, score = verify_signature_pairwise(orig_path, test_path)

    return jsonify({'result': result, 'score': score}), 200


@main.route('/classify_image', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    save_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'data', 'tests'))
    os.makedirs(save_dir, exist_ok=True)
    filename = secure_filename(f.filename)
    path = os.path.join(save_dir, filename)
    f.save(path)

    try:
        result = predict_signature(path)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500