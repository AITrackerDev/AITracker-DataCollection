# This is the data collection application of our program
# All this does is take a picture and saves it to the folder "data_images"
import customtkinter as ctk
import h5py
import numpy as np
import cv2
import random as rand
import math
from PIL import Image, ImageTk

# application setup variables
WIDTH, HEIGHT = 1080, 720
ASSETS_PATH = "assets/"
current_frame = 0

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

# dot information
dot_picture = Image.open(ASSETS_PATH + "dot.png")
dot_image = ImageTk.PhotoImage(dot_picture)
dot_x = 0
dot_y = 0
current_direction = None

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

    #reads data from the camera
    ret, frame = cam.read()

    if ret:
        # flip image
        frame = cv2.flip(frame, 1)
        # set the current image to the flipped one
        img_frame = frame
        # convert the image so it can be displayed using the data_frame label
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        data_label.configure(image=img)
        data_label.image = img
    # after a defined number of milliseconds, run this function again
    data_label.after(7, update_camera)


# takes a picture when the space bar is pressed
def take_picture(event):
    global img_counter
    global current_frame

    # if the data frame is currently loaded, save a picture
    if current_frame == data_frame:
        generate_dot_position()
        dot_label.place(x=dot_x, y=dot_y)
        # the format for storing the images
        img_name = f'opencv_frame_{img_counter}'
        # saves the image as a png file
        cv2.imwrite(img_name + ".png", img_frame)
        print('screenshot taken')
        # the number of images automatically increases by 1
        img_counter += 1

def determine_direction(x, y):
    rect_width =  math.floor(WIDTH/3)
    rect_height = math.floor(HEIGHT/3)
    if x < rect_width and y < rect_height:
        return "north west"
    elif x < rect_width and y < 2 * rect_height and y > rect_height:
        return "west"
    elif x < rect_width and y < 3 * rect_height and y > 2 * rect_height:
        return "south west"
    elif x < 2 * rect_width and x > rect_width and y < rect_height:
        return "north"
    elif x < 2 * rect_width and x > rect_width and y < 2 * rect_height and y > rect_height:
        return "center"
    elif x < 2 * rect_width and x > rect_width and y < 3 * rect_height and y > 2 * rect_height:
        return "south"
    elif x < 3 * rect_width and x > 2 * rect_width and y < rect_height:
        return "north east"
    elif x < 3 * rect_width and x > 2 * rect_width and y < 2 * rect_height and y > rect_height:
        return "east"
    elif x < 3 * rect_width and x > 2 * rect_width and y < 3 * rect_height and y > 2 * rect_height:
        return "south east"


def generate_dot_position():
    global dot_x
    global dot_y
    dot_x = rand.randint(0, WIDTH - dot_picture.width)
    dot_y = rand.randint(0, HEIGHT - dot_picture.height)
    current_direction = determine_direction(dot_x, dot_y)
    print(current_direction)
    return current_direction

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
"""
    if data has been sent successfully
        display text that it is safe to close the app
        display button that quits the app
    else
        show loading circle animation
        show text saying it is sending
        (update when it does send)
        if it fails
            quit
"""
consent_frame.pack()
update_camera()
generate_dot_position()
dot_label.place(x=dot_x, y=dot_y)
app.mainloop()
cam.release()

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