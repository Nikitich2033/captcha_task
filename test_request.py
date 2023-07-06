import requests
import base64

# URL of the server
url = 'http://localhost:5000/api/captcha/solve'

# Read the image file and encode it to base64
with open('captcha_imgs/captcha_4.jpg', 'rb') as file:
    image_data = base64.b64encode(file.read()).decode('utf-8')

# Prepare the request payload
payload = {'image': image_data}

# Send the POST request
response = requests.post(url, json=payload)

# Check the response
if response.status_code == 200:
    result = response.json()
    print('Recognized digits:', result['Recognised digits'])
else:
    print('Error:', response.text)
