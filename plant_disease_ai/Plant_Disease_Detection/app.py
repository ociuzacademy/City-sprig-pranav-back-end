# Import libraries

import torch
from torchvision import datasets, transforms, models  # datsets  , transforms
from torch.utils.data.sampler import SubsetRandomSampler
import torch.nn as nn
import torch.nn.functional as F
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms.functional as TF
import os
import torch


# Load the model
class CNN(nn.Module):
    def __init__(self, K):
        super(CNN, self).__init__()
        self.conv_layers = nn.Sequential(
            # conv1
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(2),
            # conv2
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2),
            # conv3
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(2),
            # conv4
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(2),
        )

        self.dense_layers = nn.Sequential(
            nn.Dropout(0.4),
            nn.Linear(50176, 1024),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(1024, K),
        )

    def forward(self, X):
        out = self.conv_layers(X)

        # Flatten
        out = out.view(-1, 50176)

        # Fully connected
        out = self.dense_layers(out)

        return out

targets_size = 39
model = CNN(targets_size)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "plant_disease_model_1_latest.pt")

model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu'), weights_only=True))
model.eval()


# Load other details
csv_path = os.path.join(os.path.dirname(__file__), 'disease_info.csv')
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

disease_info = pd.read_csv(csv_path, encoding='cp1252')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'supplement_info.csv')

supplement_info = pd.read_csv(csv_path, encoding='cp1252')




# Read input image
# You may edit the image name to read different images  in the folder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(BASE_DIR, "test_images", "grape_black_rot.JPG")

image = Image.open(image_path)

# Make prediction
image = image.resize((224, 224))
input_data = TF.to_tensor(image)
input_data = input_data.view((-1, 3, 224, 224))
output = model(input_data)
output = output.detach().numpy()
pred = np.argmax(output)
disease = disease_info['disease_name'][pred]
description =disease_info['description'][pred]
prevention = disease_info['Possible Steps'][pred]
supplement_name = supplement_info['supplement name'][pred]
supplement_buy_link = supplement_info['buy link'][pred]


# Get result
print("Detected Disease is: ", disease)
print()
print("Description of the disease: ", description)
print()
print("Prevention methods are: ", prevention)
print()
print("Suppliment to prevent is: ", supplement_name)
print()
print("Link to buy suppliment is ", supplement_buy_link)


import os
import torch
from PIL import Image
import torchvision.transforms as transforms

# Load the AI model from the correct path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "plant_disease_model_1_latest.pt")
model = CNN(targets_size)
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu'), weights_only=True))
model.eval()

def predict_disease(image_path):
    image = Image.open(image_path)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)

    pred_index = output.argmax(1).item()  # Get the predicted index

    # Retrieve disease information using the index
    disease = disease_info['disease_name'][pred_index]
    description = disease_info['description'][pred_index]
    prevention = disease_info['Possible Steps'][pred_index]
    supplement_name = supplement_info['supplement name'][pred_index]
    supplement_buy_link = supplement_info['buy link'][pred_index]

    return {
        "disease": disease,
        "description": description,
        "prevention": prevention,
        "supplement": supplement_name,
        "buy_link": supplement_buy_link
    }