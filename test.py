import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Open the webcam
cap = cv2.VideoCapture(0)

# Load the Haar cascades for eyes
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def update():
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale for better performance
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the frame
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangles around the eyes
    for (ex, ey, ew, eh) in eyes:
        if len(eyes) == 2:
            cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    # Convert the frame to RGB format
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the image to match the label dimensions
    resized_image = cv2.resize(rgb_image, (label.winfo_width(), label.winfo_height()))

    # Convert the resized frame to ImageTk format
    img = Image.fromarray(resized_image)
    img_tk = ImageTk.PhotoImage(image=img)

    # Update the label with the new image
    label.img = img_tk
    label.config(image=img_tk)

    # Call the update function after a delay (e.g., 10 milliseconds)
    label.after(10, update)

# Create the main window
root = tk.Tk()
root.title("Eye Detection")

# Make the window fullscreen
root.attributes('-fullscreen', True)

# Create a label to display the video stream
label = tk.Label(root)
label.pack(fill=tk.BOTH, expand=True)

# Call the update function to start the video stream
update()

# Run the Tkinter main loop
root.mainloop()

# Release the camera when the application is closed
cap.release()
