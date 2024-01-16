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
        try:
            image = cv2.imread(file_path)
            if image is None:  # Check if image was successfully read
                raise ValueError("Invalid image file")

            result = recognize_faces(file_path)
            messagebox.showinfo("Face Recognition Result", result)
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("Error", f"Invalid file: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main GUI window
root = tk.Tk()
root.title("Face Recognition")
root.geometry("600x400")  # Set initial window size
root.resizable(True, True)  # Allow resizing

# Set a minimum size for the window
root.minsize(300, 200)  # Prevent the window from being smaller than 300x200 pixels

# Create an "Open Image" button
open_button = tk.Button(root, text="Open Image", command=open_image)

def center_button(event = None):
    """Centers the button within the window."""
    button_width = open_button.winfo_width()
    window_width = root.winfo_width()
    padx = (window_width - button_width) // 2

    button_height = open_button.winfo_height()
    window_height = root.winfo_height()
    pady = (window_height - button_height) // 2

    open_button.grid(row=0, column=0, padx=(padx, padx), pady=(pady, pady), sticky="nsew")

center_button()  # Center the button initially

# Bind the center_button function to window resize events
root.bind("<Configure>", center_button)

# Start the GUI main loop
root.mainloop()
