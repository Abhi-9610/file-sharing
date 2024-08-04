from flask import Blueprint, request, send_from_directory, jsonify, current_app
from . import db
from .models import File
from .utils import encrypt_filename, decrypt_filename, generate_key
import os

# Secret key for encryption
encryption_key = generate_key()

main_bp = Blueprint('main', __name__)

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    filename = file.filename
    encrypted_filename = encrypt_filename(filename, encryption_key)
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], encrypted_filename))

    new_file = File(filename=filename, encrypted_url=encrypted_filename)
    db.session.add(new_file)
    db.session.commit()

    return jsonify({'message': 'File successfully uploaded', 'encrypted_url': encrypted_filename}), 201

@main_bp.route('/download/<encrypted_url>', methods=['GET'])
def download_file(encrypted_url):
    try:
        filename = decrypt_filename(encrypted_url, encryption_key)
    except Exception as e:
        return jsonify({'error': 'Invalid URL'}), 400

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], encrypted_url, as_attachment=True, download_name=filename)
