# -*- coding: utf-8 -*-
"""imageclassification

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16w1zKn4RIyWm78lIaHXquteLSc26KXGG
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import LabelBinarizer

# Step 1: Load the data
file_path = r"/content/mnist_compressed.npz"
data = np.load(file_path)

# Inspect keys in the .npz file
print("Keys in the .npz file:", data.keys())

# Load training and test data
X_train = data['train_images']
y_train = data['train_labels']
X_test = data['test_images']
y_test = data['test_labels']

# Step 2: Display some images with their labels
def display_images(images, labels, num_images=10):
    plt.figure(figsize=(10, 2))
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(f"Label: {labels[i]}")
        plt.axis('off')
    plt.show()

# Show the first 10 training images and labels
display_images(X_train[:10], y_train[:10])

# Step 3: Preprocess the data
# Normalize the image data to [0, 1]
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

# Reshape if the data is not already in the form (samples, height, width, channels)
if len(X_train.shape) == 3:  # Assuming grayscale images
    X_train = X_train[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

# One-hot encode the labels
lb = LabelBinarizer()
y_train_one_hot = lb.fit_transform(y_train)
y_test_one_hot = lb.transform(y_test)

# Step 4: Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=X_train.shape[1:]),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(y_train_one_hot.shape[1], activation='softmax')
])

# Step 5: Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Step 6: Train the model
history = model.fit(X_train, y_train_one_hot,
                    validation_split=0.2,
                    epochs=10,
                    batch_size=32)

# Step 7: Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test_one_hot)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# Step 8: Predict and display output
predictions = model.predict(X_test)
predicted_labels = lb.inverse_transform(predictions)
true_labels = y_test  # Already in integer form

def display_predictions(images, true_labels, predicted_labels, num_images=10):
    plt.figure(figsize=(10, 2))
    for i in range(num_images):
        plt.subplot(1, num_images, i + 1)
        plt.imshow(images[i].squeeze(), cmap='gray')
        plt.title(f"T: {true_labels[i]}\nP: {predicted_labels[i]}")
        plt.axis('off')
    plt.show()

# Show the first 10 test images, true labels, and predictions
display_predictions(X_test[:10], true_labels[:10], predicted_labels[:10])

# Step 9: Save the model
model.save('mnist_cnn_model.h5')