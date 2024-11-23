# -*- coding: utf-8 -*-
"""Facial recognition_6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dmoRYxbGBKKB7mr5aP43sHnI3IKxJpMr
"""

import os
import cv2
import numpy as np
from deepface import DeepFace
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt


def extract_embeddings(image_path):
    try:
        embedding = DeepFace.represent(img_path=image_path, model_name="Facenet", enforce_detection=False)
        return embedding[0]["embedding"]
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def prepare_data(dataset_path):
    embeddings = []
    labels = []

    for label in os.listdir(dataset_path):
        label_path = os.path.join(dataset_path, label)
        if not os.path.isdir(label_path):
            continue

        for image_name in os.listdir(label_path):
            image_path = os.path.join(label_path, image_name)
            embedding = extract_embeddings(image_path)
            if embedding is not None:
                embeddings.append(embedding)
                labels.append(label)

    return np.array(embeddings), np.array(labels)


dataset_path = r"C:\Users\Anjali\Downloads\Face_recognition\Celebrity Faces Dataset"


print("Preparing dataset...")
X, y = prepare_data(dataset_path)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print("Training model...")
clf = SVC(kernel="linear", probability=True)
clf.fit(X_train, y_train)


print("Evaluating model...")
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))


def predict_celebrity(image_path):
    embedding = extract_embeddings(image_path)
    if embedding is not None:
        prediction = clf.predict([embedding])[0]
        probabilities = clf.predict_proba([embedding])[0]
        return prediction, probabilities
    else:
        return None, None


test_image = r"C:\Users\Anjali\Downloads\Face_recognition\Celebrity Faces Dataset\Tom Cruise\091_a9736a22.jpg"
predicted_label, probabilities = predict_celebrity(test_image)
if predicted_label:
    print(f"Predicted: {predicted_label}")
    print(f"Probabilities: {probabilities}")
    img = cv2.imread(test_image)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Prediction: {predicted_label}")
    plt.axis("off")
    plt.show()
else:
    print("Could not process the image.")

test_image = r"C:\Users\Anjali\Downloads\Face_recognition\Celebrity Faces Dataset\Johnny Depp\090_c5d1d9eb.jpg"  # Replace with the path of a new image
predicted_label, probabilities = predict_celebrity(test_image)
if predicted_label:
    print(f"Predicted: {predicted_label}")
    print(f"Probabilities: {probabilities}")
    img = cv2.imread(test_image)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Prediction: {predicted_label}")
    plt.axis("off")
    plt.show()
else:
    print("Could not process the image.")

test_image = r"C:\Users\Anjali\Downloads\Face_recognition\Celebrity Faces Dataset\Brad Pitt\068_5ebbf7fb.jpg"  # Replace with the path of a new image
predicted_label, probabilities = predict_celebrity(test_image)
if predicted_label:
    print(f"Predicted: {predicted_label}")
    print(f"Probabilities: {probabilities}")
    img = cv2.imread(test_image)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(f"Prediction: {predicted_label}")
    plt.axis("off")
    plt.show()
else:
    print("Could not process the image.")
