import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN

# Create a function to recognize faces in an image
def recognize_faces(image_path):
    image = cv2.imread(image_path)
    result_image = image.copy()

    # Initialize the MTCNN face detection model
    detector = MTCNN()

    # Detect faces in the image
    faces = detector.detect_faces(image)

    if faces:
        # Draw bounding boxes around detected faces
        for face in faces:
            x, y, width, height = face['box']
            cv2.rectangle(result_image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Display the image with bounding boxes
        cv2.imshow('Detected Faces', result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return f"Number of faces detected: {len(faces)}"
    else:
        return "No faces found"

# Create a function to open an image and perform face recognition
def open_image():
    file_path = filedialog.askopenfilename()
    
    if file_path:
        result = recognize_faces(file_path)
        messagebox.showinfo("Face Recognition Result", result)

# Create the main GUI window
root = tk.Tk()
root.title("Face Recognition")

# Create an "Open Image" button
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

# Start the GUI main loop
root.mainloop()
