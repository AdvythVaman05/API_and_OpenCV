import os
import cv2
from flask import jsonify

# Function to process the image
def process_image(filename):
    # Define the input and output folders
    INPUT_FOLDER = 'input_images'
    OUTPUT_FOLDER = 'output_images'

    # Ensure the output folder exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Construct the full path for the input and output files
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f'grayscale_{filename}')

    # Check if the input file exists
    if not os.path.exists(input_path):
        return jsonify({"error": "File not found"}), 404

    # Load the image
    image = cv2.imread(input_path)

    if image is None:
        return jsonify({"error": "Invalid image format"}), 400

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image to the output folder
    cv2.imwrite(output_path, gray_image)

    return jsonify({"message": "Image processed successfully", "output_path": output_path}), 200
