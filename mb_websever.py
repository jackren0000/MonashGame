# -*- coding: utf-8 -*-
"""MB_webSever

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A4YzjeqqKXJuVEOWX2h1S40LwtTM_xaw

**Mount to Google Drive**
"""

import openai
openai.api_key = 'J527boZKu6VhG9eqV469T3BlbkFJPh2iqLOqB8sMSPifW4EV'

def generate_next_step(prompt, action):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{prompt}\n{action}\n",
        temperature=0.6,
        max_tokens=150
    )

    return response.choices[0].text.strip()






# flask is a Python library that lets you develop web servers.
from flask import Flask, request, jsonify, send_from_directory
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

  def forward(self, x):
    # Pass the first convolutional layer
    x = self.pool_1(F.relu(self.conv1(x)))

    # Pass the second convolutional layer
    x = self.pool_2(F.relu(self.conv2(x)))

    # Flatten x into one dimension
    x = torch.flatten(x, 1)

    # Pass the fully connected layer
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)

    return x

  def predict(self, x):
    predictions = self(x)

    # Get the predicted classes
    _, predicted_classes = torch.max(predictions, dim=1)

    return predicted_classes, x
      
# Instantiate your model and load its weights
model = CNN()
model.load_state_dict(torch.load('CNN_model.pth'))
model.eval()

app = Flask(__name__)

# If there is a GET request to the root of the router, execute index() function.
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')

# If there is a POST request to the predict endpoint of the router, execute predict() function
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
  prediction = predicted.item()
    
  # Instead of directly returning a pre-written story part, we will generate it using OpenAI's API.
  # For simplicity, let's say that the 'action' is the name of the predicted building.
  building_name = building_names[prediction]
  story_part = generate_next_step("You are standing in front of a building.", f"I decided to enter the {building_name}.")

    
  return jsonify({'prediction': prediction, 'story': story_part})

if __name__ == '__main__':
  app.run(debug = True)
