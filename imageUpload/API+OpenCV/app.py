import os
import cv2
from flask import Flask, request, send_from_directory, jsonify, render_template

app = Flask(__name__)

# Directories for file storage
UPLOAD_FOLDER = 'uploads'
INPUT_FOLDER = 'input_images'
OUTPUT_FOLDER = 'output_images'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Function to process the image to grayscale
def process_image(filename):
    input_path = os.path.join(app.config['INPUT_FOLDER'], filename)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f'grayscale_{filename}')

    if not os.path.exists(input_path):
        return jsonify({"error": "File not found"}), 404

    # Load the image
    image = cv2.imread(input_path)

    if image is None:
        return jsonify({"error": "Invalid image format"}), 400

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite(output_path, gray_image)

    return jsonify({"message": "Image processed successfully", "output_path": output_path}), 200

# Route for the upload page
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading images
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No selected file')

    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Move the file to input_images for processing
    input_path = os.path.join(app.config['INPUT_FOLDER'], file.filename)
    os.rename(file_path, input_path)

    # Process the image to grayscale
    response, status_code = process_image(file.filename)
    if status_code != 200:
        return render_template('index.html', error='Error processing image')

    # Get the filename of the processed image
    processed_filename = f'grayscale_{file.filename}'

    # Render the same page with the processed image displayed
    return render_template('index.html', processed_image=processed_filename)


# Route for accessing original images
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route for accessing processed images
@app.route('/output/<filename>', methods=['GET'])
def get_processed_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
