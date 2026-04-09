import requests
import base64
import cv2
import numpy as np

img = np.zeros((100, 100, 3), dtype=np.uint8)
cv2.circle(img, (50, 50), 30, (255, 255, 255), -1)
_, buffer = cv2.imencode('.png', img)
img_str = base64.b64encode(buffer).decode('utf-8')
data_uri = "data:image/png;base64," + img_str

try:
    response = requests.post('http://localhost:5000/analyze', json={'image': data_uri})
    print(response.json())
except Exception as e:
    print(e)
