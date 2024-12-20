# -*- coding: utf-8 -*-
"""Image Registration_3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1puMYw3nUQwNIKGEuw6oI5AGGpkfvPx8a
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

class ImageRegistration:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.images = self.load_dataset()

    def load_dataset(self):
        # Load all images in the dataset path
        images = []
        for file_name in os.listdir(self.dataset_path):
            img_path = os.path.join(self.dataset_path, file_name)
            img = cv2.imread(img_path)
            if img is not None:
                images.append((file_name, img))
            else:
                print(f"Could not load image: {file_name}")
        return images

    def translate(self, image, tx, ty):
        rows, cols = image.shape[:2]
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        translated_image = cv2.warpAffine(image, translation_matrix, (cols, rows))
        return translated_image

    def rotate(self, image, angle, scale=1.0):
        rows, cols = image.shape[:2]
        center = (cols // 2, rows // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
        return rotated_image

    def scale(self, image, sx, sy):
        rows, cols = image.shape[:2]
        scaling_matrix = np.float32([[sx, 0, 0], [0, sy, 0]])
        scaled_image = cv2.warpAffine(image, scaling_matrix, (cols, rows))
        return scaled_image

    def shear(self, image, shx, shy):
        rows, cols = image.shape[:2]
        shearing_matrix = np.float32([[1, shx, 0], [shy, 1, 0]])
        sheared_image = cv2.warpAffine(image, shearing_matrix, (cols, rows))
        return sheared_image

    def reflect(self, image, axis):
        rows, cols = image.shape[:2]
        if axis == 0:  # Reflect over x-axis
            reflection_matrix = np.float32([[1, 0, 0], [0, -1, rows]])
        elif axis == 1:  # Reflect over y-axis
            reflection_matrix = np.float32([[-1, 0, cols], [0, 1, 0]])
        else:
            print("Invalid axis. Use 0 for x-axis and 1 for y-axis.")
            return image
        reflected_image = cv2.warpAffine(image, reflection_matrix, (cols, rows))
        return reflected_image

    def save_image(self, image, output_path):
        cv2.imwrite(output_path, image)

    def apply_transformation(self, choice, save_output=False, **kwargs):
        methods = {
            1: ('Translation', lambda img: self.translate(img, kwargs.get('tx', 0), kwargs.get('ty', 0))),
            2: ('Rotation', lambda img: self.rotate(img, kwargs.get('angle', 0), kwargs.get('scale', 1.0))),
            3: ('Scaling', lambda img: self.scale(img, kwargs.get('sx', 1.0), kwargs.get('sy', 1.0))),
            4: ('Shearing', lambda img: self.shear(img, kwargs.get('shx', 0), kwargs.get('shy', 0))),
            5: ('Reflection', lambda img: self.reflect(img, kwargs.get('axis', 0)))
        }

        if choice in methods:
            method_name, transform_func = methods[choice]
            output_dir = os.path.join(self.dataset_path, f"{method_name}_output")
            if save_output and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for file_name, img in self.images:
                transformed_image = transform_func(img)
                if save_output:
                    output_path = os.path.join(output_dir, f"transformed_{file_name}")
                    self.save_image(transformed_image, output_path)
                else:
                    self.visualize(img, transformed_image, f"{method_name} - {file_name}")

            print(f"Transformation applied to all images. Results {'saved to ' + output_dir if save_output else 'displayed.'}")
        else:
            print("Invalid choice. Please select a valid transformation.")

    def visualize(self, original, transformed, title):
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB))
        plt.title(f'Transformed Image: {title}')
        plt.axis('off')

        plt.show()

def menu():
    # Hardcoded dataset path
    dataset_path = r"C:\Users\Anjali\Downloads\image_registration_dataset"

    if not os.path.exists(dataset_path):
        print("Invalid dataset path. Please check the hardcoded path in the code.")
        return

    ir = ImageRegistration(dataset_path)

    if not ir.images:
        print("No valid images found in the dataset.")
        return

    while True:
        print("\nImage Registration Techniques:")
        print("1. Translation")
        print("2. Rotation")
        print("3. Scaling")
        print("4. Shearing")
        print("5. Reflection")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice (1-6): "))

            if choice == 6:
                print("Exiting the program.")
                break

            save = input("Do you want to save the results? (yes/no): ").strip().lower() == 'yes'

            if choice == 1:
                tx = float(input("Enter translation along x-axis: "))
                ty = float(input("Enter translation along y-axis: "))
                ir.apply_transformation(choice, save_output=save, tx=tx, ty=ty)

            elif choice == 2:
                angle = float(input("Enter rotation angle: "))
                scale = float(input("Enter scaling factor (default 1.0): ") or "1.0")
                ir.apply_transformation(choice, save_output=save, angle=angle, scale=scale)

            elif choice == 3:
                sx = float(input("Enter scaling factor for x-axis: "))
                sy = float(input("Enter scaling factor for y-axis: "))
                ir.apply_transformation(choice, save_output=save, sx=sx, sy=sy)

            elif choice == 4:
                shx = float(input("Enter shearing factor for x-axis: "))
                shy = float(input("Enter shearing factor for y-axis: "))
                ir.apply_transformation(choice, save_output=save, shx=shx, shy=shy)

            elif choice == 5:
                axis = int(input("Enter reflection axis (0 for x-axis, 1 for y-axis): "))
                ir.apply_transformation(choice, save_output=save, axis=axis)

            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    menu()

