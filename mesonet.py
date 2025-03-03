# -*- coding: utf-8 -*-
"""MesoNet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ViFOL_e5GZsfl4cgnhkn9NBMYlFUitFO
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

# Check if GPU is available and use it
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 1. Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 2. Define Paths for Your Datasets
train_data_dir = '/content/drive/MyDrive/6k_800_800/Train'
val_data_dir = '/content/drive/MyDrive/6k_800_800/Valiadation'
test_data_dir = '/content/drive/MyDrive/6k_800_800/Test'

# Debugging: Print directory contents to verify
print("Checking dataset directories...")
print("Train Directory Contents:", os.listdir(train_data_dir))
print("Validation Directory Contents:", os.listdir(val_data_dir))
print("Test Directory Contents:", os.listdir(test_data_dir))

# 3. Data Preprocessing with Augmentation
transform_train = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

transform_val_test = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# 4. Load Datasets
print("Loading datasets...")
train_dataset = datasets.ImageFolder(root=train_data_dir, transform=transform_train)
val_dataset = datasets.ImageFolder(root=val_data_dir, transform=transform_val_test)
test_dataset = datasets.ImageFolder(root=test_data_dir, transform=transform_val_test)

# Create DataLoaders
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

print("Datasets loaded successfully!")

# 5. Define the MesoNet Model
class MesoNet(nn.Module):
    def __init__(self):
        super(MesoNet, self).__init__()
        # First Convolutional Block
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=3, padding=1),
            nn.BatchNorm2d(8),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        # Second Convolutional Block
        self.layer2 = nn.Sequential(
            nn.Conv2d(8, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        # Fully Connected Layers
        self.fc1 = nn.Linear(16 * 32 * 32, 16)  # Adjust input size based on image dimensions
        self.fc2 = nn.Linear(16, 2)  # Binary classification (Real vs Fake)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = x.view(x.size(0), -1)  # Flatten for fully connected layers
        x = self.fc1(x)
        x = self.fc2(x)
        return x

# Initialize the MesoNet model
model = MesoNet().to(device)
print(model)

# Weighted Loss Function (to address class imbalance)
class_weights = torch.tensor([1.0, 2.0])  # Adjust weights as per class distribution
criterion = nn.CrossEntropyLoss(weight=class_weights.to(device))

# Optimizer and Scheduler
optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-5)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# 6. Training Function with Early Stopping
def train_model(model, train_loader, val_loader, criterion, optimizer, scheduler, num_epochs=20, patience=3):
    best_val_loss = float('inf')
    patience_counter = 0

    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        model.train()
        running_loss, correct, total = 0.0, 0, 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item()
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        train_loss = running_loss / len(train_loader)
        train_acc = correct / total * 100
        val_loss, val_acc = validate_model(model, val_loader, criterion)

        print(f"Train Loss: {train_loss:.4f}, Train Accuracy: {train_acc:.2f}%")
        print(f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_acc:.2f}%")

        # Check for early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            torch.save(model.state_dict(), "MesoNet_model.pth")
            print("Best model saved!")
        else:
            patience_counter += 1

        if patience_counter >= patience:
            print("Early stopping triggered!")
            break

        scheduler.step()

# 7. Validation Function
def validate_model(model, val_loader, criterion):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)
            running_loss += loss.item()
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    val_loss = running_loss / len(val_loader)
    val_acc = correct / total * 100
    return val_loss, val_acc

# 8. Train and Validate the Model
print("Starting training...")
train_model(model, train_loader, val_loader, criterion, optimizer, scheduler, num_epochs=20, patience=3)
print("Training completed!")

# 9. Testing and Predicting on New Images
def predict(model, test_loader):
    model.eval()
    class_names = ["Real", "Fake"]
    predictions = []

    print("\nTesting the model...")
    with torch.no_grad():
        for inputs, _ in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            predictions.append(preds.item())
            print(f"Prediction: {class_names[preds.item()]}")

    return predictions

# Run prediction on the test set
model.load_state_dict(torch.load("MesoNet_model_new_dataset.pth"))
predictions = predict(model, test_loader)

# 10. Evaluate the Model
true_labels = []
predicted_labels = []

with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        true_labels.extend(labels.cpu().numpy())
        predicted_labels.extend(preds.cpu().numpy())

true_labels = np.array(true_labels)
predicted_labels = np.array(predicted_labels)

print("Classification Report:")
print(classification_report(true_labels, predicted_labels, target_names=["Real", "Fake"]))

cm = confusion_matrix(true_labels, predicted_labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Real", "Fake"])
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.show()

from google.colab import drive
drive.mount('/content/drive')
