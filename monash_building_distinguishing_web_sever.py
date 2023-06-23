# -*- coding: utf-8 -*-
"""Monash Building distinguishing web sever

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A4YzjeqqKXJuVEOWX2h1S40LwtTM_xaw

**Mount to Google Drive**
"""

# flask is a Python library that lets you develop web servers.
from flask import Flask, request
import torch
from PIL import Image
from torchvision import transforms

app = Flask(__name__)
model = torch.load('CNN_model.pth')

@app.route('/predict', methods=['POST'])
def predict():
  file= request.files['file']
  image = Image.open(file.stream)
  transform = transforms.Compose(
      [transforms.Resize((224, 224)),
       transforms.ToTensor()])
  image = transform(image)
  image = image.unsqueeze(0)
  output = model(image)
  _, predicted = torch.max(output, 1)
  return {'prediction': int(predicted)}

if __name__ == '__main__':
  app.run(debug = True)

