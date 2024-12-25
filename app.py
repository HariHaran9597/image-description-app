from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import io
import tensorflow as tf
from transformers import AutoImageProcessor, TFAutoModelForImageClassification
import os

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend')

# Load the pre-trained model and processor from Hugging Face
model_name = "microsoft/resnet-50"
processor = AutoImageProcessor.from_pretrained(model_name)
model = TFAutoModelForImageClassification.from_pretrained(model_name)

print("Model loaded successfully!")

# Function to preprocess the image
def preprocess_image(image_data):
    image = Image.open(io.BytesIO(image_data)).convert("RGB")
    inputs = processor(images=image, return_tensors="tf")
    return inputs

# Function to get image description using the model
def get_image_description(image_data):
    inputs = preprocess_image(image_data)

    # Perform inference
    outputs = model(**inputs)
    logits = outputs.logits

    # Convert logits to probabilities and find the most likely class
    probabilities = tf.nn.softmax(logits, axis=-1)
    predicted_class_id = int(tf.argmax(probabilities, axis=-1)[0])

    # The model was trained on ImageNet-1k; use the labels from the model's config
    predicted_label = model.config.id2label[predicted_class_id]
    return predicted_label

# Route to serve the main HTML file
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route to serve other static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# API endpoint to handle image uploads and return descriptions
@app.route('/describe', methods=['POST'])
def describe_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image_data = file.read()

    try:
        description = get_image_description(image_data)
        return jsonify({'description': description})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Use debug=True for development only
