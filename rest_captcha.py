from tensorflow.keras.models import load_model
import cv2
import numpy as np
from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

mnist_model = load_model("mnist_model.h5")  

def segment_img(input_img):
    
    # Convert the PIL Image to a NumPy array
    image_array = np.array(input_img)

    
    # Обработка изображения
    # Преобразование из RGB в оттенки серого
    img = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

    # Адаптивная бинаризация
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 17, 2)

    # Оцу-бинаризация
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Оцу-бинаризация с гауссовым размытием
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((3,3), np.uint8)

    dilation = cv2.dilate(th3, kernel, iterations=1)

    erosion = cv2.erode(dilation, kernel, iterations=1)

    kernel = np.ones((3,1), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    # Get individual letters
    x, y, w, h = 22, 10, 20, 38
    segments = []
    for i in range(6):
        # Get the bounding rectangle

        # Save each character as a separate image
        # Change dilation to img if you want to preserve the original color
        digit = dilation[y:y + h, x:x + w]

        # Add a white border of 5 pixels
        digit = cv2.copyMakeBorder(digit, 5, 5, 5, 5, cv2.BORDER_CONSTANT, value=[255, 255, 255])

        # Convert the digit to PIL Image
        digit_pil = Image.fromarray(digit)

        # Append the digit to the list of segments
        segments.append(digit_pil)

        x += w

    return segments


@app.route('/api/captcha/solve', methods=['POST'])
def solve_captcha():
    try:
        # Get image data from the request
        data = request.json
        image_data = data['image']
        
        # Decode image from base64 and create an Image object
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Segment the image
        segmented_images = segment_img(image)
        
        recognized_text = ""
        for segment in segmented_images:
            # Preprocess the segment
            # Convert the PIL Image to a NumPy array
            segment = np.array(segment)
            segment = cv2.resize(segment, (28, 28))
            segment = np.invert(np.array([segment]))
            
            # Predict the digit using the pre-trained Keras MNIST model
            digit = mnist_model.predict(segment)
            
            # Append the recognized digit to the recognized text
            recognized_text += str(np.argmax(digit))
        
        # Return the recognized text as the response
        return jsonify({'Recognised digits': recognized_text})
    
    except Exception as e:
        # Handle errors
        print('Error:', str(e))
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run()