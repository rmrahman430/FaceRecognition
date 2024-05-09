import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from deepface import DeepFace

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'fastmtcnn',
]

# Create a function to recognize faces in an image
def recognize_faces(image_path):
    image = cv2.imread(image_path)
    result_image = image.copy()

    try:
        results = DeepFace.analyze(image, actions=["age", "gender", "race", "emotion"])
        print(results)

        for face in results:
            x, y, width, height = face['region'].values()

            # Access attributes for the current face
            age = face['age']
            gender = face['dominant_gender']
            race = face['dominant_race']
            emotion = face['dominant_emotion']

            # Adjust text placement to be below the rectangle
            text_offset = 10  # Adjust this value for vertical spacing
            cv2.putText(result_image, f"Age: {age}", (x, y + height + text_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(result_image, f"Gender: {gender}", (x, y + height + text_offset * 2), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(result_image, f"Race: {race}", (x, y + height + text_offset * 3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(result_image, f"Emotion: {emotion}", (x, y + height + text_offset * 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(result_image, (x, y), (x + width, y + height), (0, 255, 0), 2)

        cv2.imshow('Face Recognition Results', result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return f"Number of faces detected: {len(results)}"
    except Exception as e:
        print(f"Error during DeepFace analysis: {e}")
        return "Error: Could not perform face recognition"


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

# Define the open_camera() function
def open_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame from camera")
            break

        faces = detector.detect_faces(frame)

        # Draw bounding boxes around detected faces
        for face in faces:
            x, y, width, height = face['box']
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create the Camera button
camera_button = tk.Button(root, text="Camera", command=open_camera)   

def center_button(event=None):
    """Centers the button within the window."""
    if event:  # Check if an event object is available
        window_width = event.width
        window_height = event.height
    else:
        window_width = root.winfo_width()
        window_height = root.winfo_height()

    button_width = open_button.winfo_width()
    padx = (window_width - button_width) // 2

    button_height = open_button.winfo_height()
    pady = (window_height - button_height) // 2

    open_button.grid(row=0, column=0, padx=(padx, padx), pady=(pady, pady), sticky="nsew")
    camera_button.grid(row=1, column=0, padx=(padx, padx), pady=(pady, pady), sticky="nsew")

center_button()  # Center the button initially

# Bind the center_button function to window resize events
root.bind("<Configure>", center_button)

# Start the GUI main loop
root.mainloop()
