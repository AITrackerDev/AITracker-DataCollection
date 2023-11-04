# This is the data collection application of our program
# All this does is take a picture and saves it to the folder "data_images"
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

# application setup variables
WIDTH, HEIGHT = 1080, 720
ASSETS_PATH = "assets/"
current_frame = 0
STATIC_DOT = False

# webcam and current image frame setup
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
img_frame = 0
img_counter = 0

# app window setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry(str(WIDTH) + "x" + str(HEIGHT))
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
current_direction = True

# frame instantiations
consent_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
instructions_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
data_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)
end_frame = ctk.CTkFrame(master=app, width=WIDTH, height=HEIGHT)

# strings for the different frames
consent_string = "By continuing to use this application, you understand that the photos gathered by this application will be used to train a neural network designed to detect the direction someone is looking. Do you consent?"
instructions_string = "After clicking continue, the app will generate a random dot on the screen. While looking at it, press the space bar once, and a picture will be taken and a new dot will be generated in a new location. This process will repeat approximately 50 times. The window will automatically maximize as well."

# button functions
def load_frame(destroy_frame, next_frame):
    # sets the currentFrame variable to the one that's loaded
    global current_frame
    current_frame = next_frame
    # destroys the previous frame and loads the next one
    destroy_frame.destroy()
    next_frame.pack()

# updates the camera
def update_camera():
    global img_frame
    global img_counter
    
    #reads data from the camera
    ret, frame = cam.read()

    if ret:
        # flip image
        frame = cv2.flip(frame, 1)
        # set the current image to the flipped one
        img_frame = frame
        # convert the image, so it can be displayed using the data_frame label
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        data_label.configure(image=img)
        data_label.image = img
    # after a defined number of milliseconds, run this function again
    data_label.after(7, update_camera)
    
    if img_counter == 50: 
        load_frame(data_frame, end_frame)
        cam.release()
        '''
        write email received logic here
        '''

def take_picture(event):
    global direction
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
        cv2.imwrite(img_name, img_frame)

        # sends png as email
        sendEmail(img_name)

        current_direction = generate_dot_position()
        dot_label.place(x=dot_x, y=dot_y)
        print('screenshot taken')

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
        x_div = WIDTH/div_amount
        y_div = HEIGHT/div_amount
        
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
        if dot_y + dot_picture.height > HEIGHT:
            dot_y = HEIGHT - dot_picture.height
    current_direction = determine_direction(dot_x, dot_y)
    print(current_direction)
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
direction = generate_dot_position()
app.bind("<Key-space>", take_picture)
data_label = ctk.CTkLabel(data_frame, text="")
dot_label = ctk.CTkLabel(data_frame, text="")
dot_label.configure(image=dot_image)
data_label.grid(column=0, row=0)

# create example hdf5 file
fileW = h5py.File("example.hdf5", "w")

dataset = fileW.create_dataset("data", shape=(10,), dtype='i')

for i in range(10):
    dataset[i] = i

fileW.close()

# read example hdf5 file after it is created
fileR = h5py.File("example.hdf5", "r")

dataset = fileR["data"]
data = np.array(dataset)

fileR.close()

print("Example Data:")
print(data)

# program finished frame
finished_text = ctk.CTkLabel(text = "Thank you for helping us collect data for our neural network! The app will close automatically when the data has finished sending.")
finished_text.place(relx=.5, rely=.5, anchor=ctk.CENTER)

# application start code
consent_frame.pack()
update_camera()
current_direction = generate_dot_position()
dot_label.place(x=dot_x, y=dot_y)
app.mainloop()

# def take_picture(event):
#     global n_counter
#     global nw_counter
#     global ne_counter
#     global w_counter
#     global e_counter
#     global sw_counter
#     global se_counter
#     global s_counter
#     global c_counter
#     global current_frame
#     global img_name
#
#     n_counter = 0
#     nw_counter = 0
#     ne_counter = 0
#     w_counter = 0
#     e_counter = 0
#     sw_counter = 0
#     se_counter = 0
#     s_counter = 0
#     c_counter = 0
#
#
#     #if the data frame is currently loaded, save a picture
#     if current_frame == data_frame:
#         direction = d #generate_dot_position()
#         dot_label.place(x=dot_x, y=dot_y)
#         # the format for storing the images
#
#         if direction == "north":
#             n_counter += 1
#             img_name = f'north{n_counter}'
#         elif direction == "north west":
#             nw_counter += 1
#             img_name = f'northwest{nw_counter}'
#         elif direction == "north east":
#             ne_counter += 1
#             img_name = f'northeast{ne_counter}'
#         elif direction == "west":
#             w_counter += 1
#             img_name = f'west{w_counter}'
#         elif direction == "south west":
#             sw_counter += 1
#             img_name = f'southwest{sw_counter}'
#         elif direction == "south east":
#             se_counter += 1
#             img_name = f'southeast{se_counter}'
#         elif direction == "south":
#             s_counter += 1
#             img_name = f'south{s_counter}'
#         elif direction == "center":
#             c_counter += 1
#             img_name = f'center{c_counter}'
#
#         # saves the image as a png file
#         cv2.imwrite(img_name + ".png", img_frame)
#         print('screenshot taken')

# takes a picture when the space bar is pressed
# def take_picture(event):
#     global img_counter
#     global current_frame
#
#     # if the data frame is currently loaded, save a picture
#     if current_frame == data_frame:
#         generate_dot_position()
#         dot_label.place(x=dot_x, y=dot_y)
#         # the format for storing the images
#         img_name = f'opencv_frame_{img_counter}'
#         # saves the image as a png file
#         cv2.imwrite(img_name + ".png", img_frame)
#         print('screenshot taken')
#         # the number of images automatically increases by 1
#         img_counter += 1