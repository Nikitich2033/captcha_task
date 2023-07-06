import requests
import base64

# URL of the server
url = 'http://localhost:5000/api/captcha/solve'

# Load the image and encode it to base64
with open('captcha_imgs/captcha_0.jpg', 'rb') as file:
    image_data = file.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')

# Prepare the request payload
payload = {'image': encoded_image}

# Send the POST request
response = requests.post(url, json=payload)

# Check the response
if response.status_code == 200:
    result = response.json()
    print('Recognized text:', result['text'])
else:
    print('Error:', response.text)
