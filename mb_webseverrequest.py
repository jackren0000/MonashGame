# -*- coding: utf-8 -*-
"""MB_webSeverRequest

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_OGE8qcy2oUfqjJ_GqEGxZq8T5R-RsoC
"""

import requests

# The local URL where the Flask app is running
url = "http://127.0.0.1:5000/predict"

# Open and read the image file
with open('/train/Monash Hargrave Andrew Library/img0.jpg', 'rb') as f:
    img = f.read()

# Create a dictionary to send in the HTTP request
files = {"file": img}

# Send the POST request
response = requests.post(url, files=files)

# Print the prediction
print(response.json())
