# -*- coding: utf-8 -*-
"""MB_webSever

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

import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
  def __init__(self, num_classes = 3):
    super().__init__()
    # First convolutional layer
    self.conv1 = nn.Conv2d(3, 6, 5)
    self.pool_1 = nn.MaxPool2d(2, 2)

    # Second convolutional layer
    self.conv2 = nn.Conv2d(6, 16, 5)
    self.pool_2 = nn.MaxPool2d(2, 2)

    # Fully connected layer
    self.fc1 = nn.Linear(53 * 53 * 16, 120)
    self.fc2 = nn.Linear(120, 84)
    self.fc3 = nn.Linear(84, 3)

# Instantiate your model and load its weights
model = CNN()
model.load_state_dict(torch.load('CNN_model.pth'))
model.eval()

app = Flask(__name__)

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
  return jsonify({'prediction': prediction})

if __name__ == '__main__':
  app.run(debug = True)
