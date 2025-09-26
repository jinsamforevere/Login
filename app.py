from flask import Flask, request, send_from_directory, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route - Role selection
@app.route('/')
def index():
    return render_template('index.html')

# Teacher dashboard
@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

# Student dashboard
@app.route('/student')
def student():
    return render_template('student.html')

# Upload file (Teacher)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({'message': f'File {filename} uploaded successfully!'})

# List all files (Student)
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

# Download file (Student)
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
