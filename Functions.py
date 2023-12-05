from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import datetime
import cv2
import numpy as np
import os
import h5py
import matplotlib.pyplot as plt
import dlib

EYES_DETECTOR = dlib.get_frontal_face_detector()
LANDMARK_PREDICTOR = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def sendEmail(path):
    subject = "AI_Data"
    body = "AI Training Data"
    sender = "eyetrackerdata@gmail.com"
    recipients = "eyetrackercollection@gmail.com"
    password = "kjio oydv zphc tkdi"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = sender

    # storing the receivers email address
    msg['To'] = recipients

    # storing the subject
    msg['Subject'] = subject

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = path
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('image', 'plain')

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(sender, password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(sender, recipients, text)

    # terminating the session
    s.quit()

def createH5():
    # Define the path to the folder
    folder_path = 'images'

    # Ensure it's a directory
    if os.path.isdir(folder_path):
        # Loop through all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if it's an image file
            if filename.endswith('.png') and filename.startswith('crop'):
                # Read the image
                image = cv2.imread(file_path)

                # Convert the image to grayscale
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Save the grayscale image with the desired filename format
                output_filename = f'g-{os.path.splitext(filename)[0]}.png'
                output_path = os.path.join(folder_path, output_filename)
                cv2.imwrite(output_path, grayscale_image)

    common_size = (190, 80)

    # Create a list to store resized images and labels
    resized_images = []
    labels = []

    # Loop through the files in the directory
    for filename in os.listdir(folder_path):
        if filename.startswith('g-') and filename.endswith('.png'):
            # Load the image using cv2 and resize it to the specified dimension
            img = cv2.imread(os.path.join(folder_path, filename))
            img = cv2.resize(img, common_size)
            resized_images.append(img)

            # Use the filename (without extension) as the label
            label = os.path.splitext(filename)[0]
            labels.append(label)

    # Convert the lists to NumPy arrays
    resized_images = np.array(resized_images)
    labels = np.array(labels, dtype='S')

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time to create a timestamp
    timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Create a file name using the timestamp
    h5path = f"image_collection{timestamp}.h5"
    h5f = h5py.File(h5path, 'w')

    # Create datasets for resized images and labels
    h5f.create_dataset('images', data=resized_images)
    h5f.create_dataset('labels', data=labels)

    # Close the HDF5 file
    h5f.close()

    # Return path of h5 file
    return h5path

def readH5(path):
    # Open the HDF5 file for reading
    h5f = h5py.File(path, 'r')

    # Read the 'images' and 'labels' datasets
    images = h5f['images'][:]
    labels = h5f['labels'][:]

    # Close the HDF5 file
    h5f.close()

    # Display the images
    for i in range(len(images)):
        label = labels[i].decode()  # Decode the label from bytes to string
        plt.figure()
        plt.imshow(images[i])
        plt.title(f"Label: {label}")
        plt.show()
        
def crop_eyes(image):
    # grayscale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # dlib faces and landmarks
    faces = EYES_DETECTOR(gray)
    landmarks = LANDMARK_PREDICTOR(gray, faces[0])
    
    pad = 5
    
    left_eye = (
        #left width, top height
        landmarks.part(36).x - pad, landmarks.part(37).y - pad,
        #right width, bottom height
        landmarks.part(39).x + pad, landmarks.part(41).y + pad
    )
    
    right_eye = (
        #left width, top height
        landmarks.part(42).x - pad, landmarks.part(43).y - pad,
        #right width, bottom height
        landmarks.part(45).x + pad, landmarks.part(47).y + pad
    )
    
    # left eye midpoint information
    left_eye_height_midpoint = (left_eye[0] + left_eye[2]) // 2
    left_eye_width_midpoint = (left_eye[1] + left_eye[3]) // 2
    
    # right eye midpoint information
    right_eye_height_midpoint = (right_eye[0] + right_eye[2]) // 2
    right_eye_width_midpoint = (right_eye[1] + right_eye[3]) // 2
    
    # [start_y:end_y, start_x:end_x]
    left_eye_region = gray[left_eye[1]:left_eye[3], left_eye[0]:left_eye[2]]
    right_eye_region = gray[right_eye[1]:right_eye[3], right_eye[0]:right_eye[2]]
    
    return (left_eye_region, right_eye_region)

def eye_template(left_eye, right_eye, output_path):
    # Resize images to have the same height
    height = max(left_eye.shape[0], right_eye.shape[0])
    # Calculate the width of the composite image
    width = left_eye.shape[1] + right_eye.shape[1]

    # Create a black background image
    composite_image = np.zeros((height, width), dtype=np.uint8)

    composite_image[:left_eye.shape[0], :left_eye.shape[1]] = left_eye
    composite_image[:right_eye.shape[0], left_eye.shape[1]:] = right_eye

    # Save the composite image in the filename
    cv2.imwrite(output_path, composite_image)