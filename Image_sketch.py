from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)

def create_sketch(image):
    scale_percent = 50
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    inverted = 255 - gray_image
    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blur = 255 - blur
    sketch = cv2.divide(gray_image, inverted_blur, scale=256.0)
    edges = cv2.Canny(resized_image, 50, 150)
    final_sketch = cv2.addWeighted(sketch, 0.8, edges, 0.2, 0)
    return final_sketch

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Read and process the image
    file_stream = io.BytesIO(file.read())
    pil_image = Image.open(file_stream).convert('RGB')
    cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    sketch = create_sketch(cv_image)

    # Convert the sketch to base64
    _, buffer = cv2.imencode('.png', sketch)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return jsonify({'sketch': img_str})

if __name__ == '__main__':
    app.run(debug=True)
