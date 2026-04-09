# FaceRead

A modern, real-time Facial Emotion Recognition web application. 
This project uses **OpenCV** to detect faces and **DeepFace** to classify emotions across 7 universal categories (Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral).

## Project Structure
- `app.py`: The Flask server that processes `/analyze` POST requests.
- `templates/index.html`: The interactive front-end UI.
- `static/`: Contains static assets like test images.

## Features
1. **Interactive Image Upload:** Drag and drop or browse to upload an image, and dynamically display bounding boxes and emotion percentage bars.
2. **Real-time Webcam Streaming:** Securely access webcam via browser, analyzing emotions locally at 2.5 frames per second using the Python backend.

## How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Backend:**
   ```bash
   python app.py
   ```

3. **Open Application**
   Navigate to [http://localhost:5000](http://localhost:5000) in your web browser.
