import os
from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
from deepface import DeepFace

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Extract base64 part separating from "data:image/jpeg;base64,"
        img_data = data['image']
        if ',' in img_data:
            img_data = img_data.split(',')[1]

        # Fix missing padding just in case
        img_data += "=" * ((4 - len(img_data) % 4) % 4)

        # Decode the image data
        img_bytes = base64.b64decode(img_data)
        
        img = None
        try:
            # Try PIL first (handles WEBP, GIF, PNG alphas, etc much better than OpenCV)
            from PIL import Image
            import io
            pil_image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            # Convert RGB to OpenCV BGR format
            img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            # Fallback to pure OpenCV
            np_arr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image format'}), 400

        # Perform analysis with DeepFace
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        
        # DeepFace.analyze returns a list of faces if multiple are found, handle first face for simplicity
        if isinstance(result, list):
            result = result[0]
            
        response = {
            'dominant_emotion': str(result.get('dominant_emotion', 'neutral')),
            'emotion_scores': {k: float(v) for k, v in result.get('emotion', {}).items() if v is not None},
            'face_box': {k: int(v) for k, v in result.get('region', {}).items() if v is not None}
        }
        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n✨ CLICK THIS LINK TO OPEN THE APP WITH CAMERA ACCESS ✨")
    print(f"👉 http://localhost:{port} 👈\n")
    app.run(debug=False, host='0.0.0.0', port=port)
