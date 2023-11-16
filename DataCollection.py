# This is the data collection application of our program
# All this does is take a picture and saves it to the folder "data_images"
import os
import shutil
import matplotlib.pyplot as plt
import customtkinter as ctk
import h5py
import numpy as np
import cv2
import random as rand
import math
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import platform
import ctypes

# app initialization
ctypes.windll.shcore.SetProcessDpiAwareness(2)
app = ctk.CTk()

if platform.system() == "Windows":
    #app.state("zoomed")
    # app.attributes('-fullscreen', True)
    app.after(0, lambda: app.state('zoomed'))
    pad=3
    # app.geometry("{0}x{1}+0+0".format(
    #     app.winfo_screenwidth()-pad, app.winfo_screenheight()-pad))
elif platform.system() == "Darwin":
    app.wm_attributes("-fullscreen", True)

# application setup variables
WIDTH, HEIGHT = app.winfo_screenwidth(), app.winfo_screenheight()
print(f"Width: {WIDTH}, Height: {HEIGHT}")
ASSETS_PATH = "assets/"
STATIC_DOT = True

# webcam and current image frame setup
global current_frame
global cam
img_frame = 0
img_counter = 0
EYE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# app window setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app.title("aiTracker Data Collection")

# counter information
n_counter = 0
nw_counter = 0
ne_counter = 0
w_counter = 0
e_counter = 0
sw_counter = 0
se_counter = 0
s_counter = 0
c_counter = 0

# dot information
dot_picture = Image.open(ASSETS_PATH + "dot.png")
dot_image = ImageTk.PhotoImage(dot_picture)
dot_x = 0
dot_y = 0

# frame instantiations
consent_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
instructions_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
data_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
end_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
current_frame = consent_frame

# strings for the different frames
consent_string = "By continuing to use this application, you understand that the photos gathered by this application will be used to train a neural network designed to detect the direction someone is looking. Do you consent?"
instructions_string = "After clicking continue, the app will generate a random dot on the screen. While looking at it, press the space bar once, and a picture will be taken and a new dot will be generated in a new location. This process will repeat approximately 50 times."
end_string = "Thank you for helping us collect data for our neural network! If you can see this message, the application is safe to close."

# create directory for images
os.mkdir("images")

def load_frame(destroy_frame, next_frame):
    # sets the currentFrame variable to the one that's loaded
    global current_frame
    global cam
    current_frame = next_frame
    # destroys the previous frame and loads the next one
    destroy_frame.destroy()
    next_frame.pack()
    
    if current_frame == data_frame:
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        update_camera()

# updates the camera
def update_camera():
    global img_frame
    global img_counter
    global current_frame
    
    #reads data from the camera
    ret, frame = cam.read()

    if ret:
        # flip image
        frame = cv2.flip(frame, 1)
        img_frame = frame
        # convert the image to grayscale for better performance
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # detect eyes in the frame
        eyes = EYE_CASCADE.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        # draw rectangles around the eyes
        for (ex, ey, ew, eh) in eyes:
            if len(eyes) <= 2:
                cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        
        # convert back to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # resize image to full screen
        img = cv2.resize(img, None, fx=WIDTH/frame.shape[1], fy=HEIGHT/frame.shape[0])
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        data_label.configure(image=img)
        #data_label.image = img
    # after a defined number of milliseconds, run this function again
    data_label.after(5, update_camera)
    
    if img_counter == 3:
        load_frame(data_frame, end_frame)
        cam.release()

        if current_frame == end_frame:
            h5path = createH5()
            sendEmail(h5path)
            readH5(h5path)

            # delete the h5 file after it has been sent
            os.remove(h5path)

def take_picture(event):
    global n_counter
    global nw_counter
    global ne_counter
    global w_counter
    global e_counter
    global sw_counter
    global se_counter
    global s_counter
    global c_counter
    global current_frame
    global img_frame
    global dot_x
    global dot_y
    global current_direction
    global img_counter

    #if the data frame is currently loaded, save a picture
    if current_frame == data_frame:
        # the format for storing the images
        img_counter += 1
        img_name = "unknown.png"
        if current_direction == "north":
            n_counter += 1
            img_name = f'north{n_counter}.png'
        elif current_direction == "north west":
            nw_counter += 1
            img_name = f'northwest{nw_counter}.png'
        elif current_direction == "north east":
            ne_counter += 1
            img_name = f'northeast{ne_counter}.png'
        elif current_direction == "west":
            w_counter += 1
            img_name = f'west{w_counter}.png'
        elif current_direction == "east":
            e_counter += 1
            img_name = f'east{e_counter}.png'
        elif current_direction == "south west":
            sw_counter += 1
            img_name = f'southwest{sw_counter}.png'
        elif current_direction == "south east":
            se_counter += 1
            img_name = f'southeast{se_counter}.png'
        elif current_direction == "south":
            s_counter += 1
            img_name = f'south{s_counter}.png'
        elif current_direction == "center":
            c_counter += 1
            img_name = f'center{c_counter}.png'

        # saves the image as a png file
        path = os.path.join('images', img_name)
        cv2.imwrite(path, img_frame)

        # crops image into left and right eyes
        image = cv2.imread(path)
        left_eye = crop_left_eye(image)
        right_eye = crop_right_eye(image)

        # create template from eye crops
        crop_path = os.path.join('images', 'crop_' + img_name)
        create_eye_template(left_eye, right_eye, crop_path)

        current_direction = generate_dot_position()
        while current_direction == "unknown":
            current_direction = generate_dot_position()

        dot_label.place(x=dot_x, y=dot_y)

def determine_direction(x, y):
    div_amount = 8
    rect_width =  math.floor(WIDTH/div_amount)
    rect_height = math.floor(HEIGHT/div_amount)
    if x < rect_width and y < rect_height:
        return "north west"
    elif x < rect_width and y < (div_amount - 1) * rect_height and y > rect_height:
        return "west"
    elif x < rect_width and y < (div_amount) * rect_height and y > (div_amount - 1) * rect_height:
        return "south west"
    elif x < (div_amount - 1) * rect_width and x > rect_width and y < rect_height:
        return "north"
    elif x < (div_amount - 5) * rect_width and x > (div_amount - 3) * rect_width and y < (div_amount - 5) * rect_height and y > (div_amount - 3) * rect_height:
        return "center"
    elif x < (div_amount - 1) * rect_width and x > rect_width and y < (div_amount) * rect_height and y > (div_amount - 1) * rect_height:
        return "south"
    elif x < 3 * rect_width and x > (div_amount - 1) * rect_width and y < rect_height:
        return "north east"
    elif x < 3 * rect_width and x > (div_amount - 1) * rect_width and y < (div_amount - 1) * rect_height and y > rect_height:
        return "east"
    elif x < (div_amount) * rect_width and x > (div_amount - 1) * rect_width and y < (div_amount) * rect_height and y > (div_amount - 1) * rect_height:
        return "south east"
    else:
        return "unknown"

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

def generate_dot_position():
    global dot_x
    global dot_y
    
    #spawns the dot at a random static point within the window
    if STATIC_DOT:
        dir = rand.randint(0, 8)
        if dir == 0:
            dot_x = 0
            dot_y = 0
        elif dir == 1:
            dot_x = (WIDTH/2) - (dot_picture.width/2)
            dot_y = 0 
        elif dir == 2:
            dot_x = WIDTH - dot_picture.width
            dot_y = 0
        elif dir == 3:
            dot_x = 0
            dot_y = (HEIGHT/2) - (dot_picture.height/2)
        elif dir == 4:
            dot_x = (WIDTH/2) - (dot_picture.width/2)
            dot_y = (HEIGHT/2) - (dot_picture.height/2)
        elif dir == 5:
            dot_x = WIDTH - dot_picture.width
            dot_y = (HEIGHT/2) - (dot_picture.height/2)
        elif dir == 6:
            dot_x = 0
            dot_y = HEIGHT - dot_picture.height
        elif dir == 7:
            dot_x = (WIDTH/2) - (dot_picture.width/2)
            dot_y = HEIGHT - dot_picture.height
        elif dir == 8:
            dot_x = WIDTH - dot_picture.width
            dot_y = HEIGHT - dot_picture.height
    else:
        #divisions of the screen
        div_amount = 8
        x_div = math.floor(WIDTH/div_amount)
        y_div = math.floor(HEIGHT/div_amount)
        
        #determines the direction to spawn the dot in 
        dir = rand.randint(0, 4)
        if dir == 0:
            dot_x = rand.randint(0, x_div)
            dot_y = rand.randint(0, HEIGHT)   
        elif dir == 1:
            dot_x = rand.randint((div_amount - 1) * x_div, WIDTH)
            dot_y = rand.randint(0, HEIGHT)
        elif dir == 2:
            dot_x = rand.randint(0, WIDTH)
            dot_y = rand.randint(0, y_div) 
        elif dir == 3:
            dot_x = rand.randint(0, WIDTH)
            dot_y = rand.randint((div_amount - 1) * y_div, HEIGHT)
        elif dir == 4:
            dot_x = rand.randint((div_amount - 5) * x_div, (div_amount - 3) * x_div)
            dot_y = rand.randint((div_amount - 5) * y_div, (div_amount - 3) * y_div)

    #check if the dot will be invisible on the screen and modify the corresponding value
    if dot_x + dot_picture.width > WIDTH:
        dot_x = WIDTH - dot_picture.width
    elif dot_x + dot_picture.width < 0:
        dot_x = 0
    if dot_y + dot_picture.height > HEIGHT:
        dot_y = HEIGHT - dot_picture.height
    elif dot_y + dot_picture.height < 0:
        dot_y = 0
    current_direction = determine_direction(dot_x, dot_y)
    return current_direction

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

def crop_left_eye(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        raise ValueError('No face detected')

    (x, y, w, h) = faces[0]

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = image[y:y+h, x:x+w]

    eyes = eye_cascade.detectMultiScale(roi_gray)

    if len(eyes) < 2:
        raise ValueError('Both eyes not detected')

    (ex1, ey1, ew1, eh1) = eyes[0]
    (ex2, ey2, ew2, eh2) = eyes[1]

    if ex1 > ex2:
        left_eye = roi_color[ey1:ey1+eh1, ex1:ex1+ew1]
    else:
        left_eye = roi_color[ey2:ey2+eh2, ex2:ex2+ew2]

    return left_eye

def crop_right_eye(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        raise ValueError('No face detected')

    (x, y, w, h) = faces[0]

    roi_gray = gray[y:y + h, x:x + w]
    roi_color = image[y:y + h, x:x + w]

    eyes = eye_cascade.detectMultiScale(roi_gray)

    if len(eyes) < 2:
        raise ValueError('Both eyes not detected')

    (ex1, ey1, ew1, eh1) = eyes[0]
    (ex2, ey2, ew2, eh2) = eyes[1]

    if ex1 > ex2:
        right_eye = roi_color[ey2:ey2 + eh2, ex2:ex2 + ew2]
    else:
        right_eye = roi_color[ey1:ey1 + eh1, ex1:ex1 + ew1]

    return right_eye

def create_eye_template(left_eye, right_eye, output_path):
    # Resize images to have the same height
    height = max(left_eye.shape[0], right_eye.shape[0])
    left_eye_resized = cv2.resize(left_eye, (0, 0), fx=height / left_eye.shape[0], fy=height / left_eye.shape[0])
    right_eye_resized = cv2.resize(right_eye, (0, 0), fx=height / right_eye.shape[0], fy=height / right_eye.shape[0])

    # Calculate the width of the composite image
    width = left_eye_resized.shape[1] + right_eye_resized.shape[1] + 35

    # Create a black background image
    composite_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Place the left and right eyes on the composite image
    composite_image[0:right_eye_resized.shape[0], 0:right_eye_resized.shape[1]] = right_eye_resized
    composite_image[0:left_eye_resized.shape[0], left_eye_resized.shape[1] + 35:] = left_eye_resized

    # Save the composite image in the filename
    cv2.imwrite(output_path, composite_image)

# widgets contained in each frame
# consent frame
consent_text = ctk.CTkLabel(consent_frame, text=consent_string)
consent_text.configure(wraplength=500)
consent_button = ctk.CTkButton(consent_frame, text="Consent", corner_radius=10,
                              command=lambda: load_frame(consent_frame, instructions_frame))
quit_button = ctk.CTkButton(consent_frame, text="Quit", corner_radius=10, command=lambda: app.destroy())

consent_text.place(relx=.5, rely=0.45, anchor=ctk.CENTER)
consent_button.place(relx=.75, rely=0.9, anchor=ctk.CENTER)
quit_button.place(relx=.25, rely=0.9, anchor=ctk.CENTER)

# instructions frame
instructions_label = ctk.CTkLabel(instructions_frame, text=instructions_string)
instructions_label.configure(wraplength=500)
instructions_button = ctk.CTkButton(instructions_frame, text="Continue", corner_radius=10,
                                   command=lambda: load_frame(instructions_frame, data_frame))

instructions_label.place(relx=.5, rely=0.45, anchor=ctk.CENTER)
instructions_button.place(relx=.5, rely=0.9, anchor=ctk.CENTER)

# data collection frame
app.bind("<Key-space>", take_picture)
data_label = ctk.CTkLabel(data_frame, text="")
dot_label = ctk.CTkLabel(data_frame, text="")
dot_label.configure(image=dot_image)
data_label.grid(column=0, row=0)

# program finished frame
finished_text = ctk.CTkLabel(end_frame, text=end_string)
finished_text.place(relx=.5, rely=.5, anchor=ctk.CENTER)

# application start code
consent_frame.pack()
current_direction = generate_dot_position()
while current_direction == "unknown":
    current_direction = generate_dot_position()

dot_label.place(x=dot_x, y=dot_y)
app.mainloop()

# removes images directory to not include them on next run of application.
shutil.rmtree("images")