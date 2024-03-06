import customtkinter as ctk
import cv2
import dlib
import numpy as np
from PIL import Image, ImageTk
import random as rand
import os

NUM_OF_IMAGES = 100

class DataScreen(ctk.CTkFrame):
    '''
    Data is collected in this screen.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        # variables for frame itself
        self._width, self._height = root.winfo_width(), root.winfo_height()
        self._screen_changer = screen_changer
        root.bind("<Key-space>", self._take_picture)
        self.focus_set()
        
        self._eyes_seen = False
        
        # image counters
        self._n_counter = 0
        self._nw_counter = 0
        self._ne_counter = 0
        self._w_counter = 0
        self._e_counter = 0
        self._sw_counter = 0
        self._se_counter = 0
        self._s_counter = 0
        self._c_counter = 0
        self._img_counter = 0
        
        # dot related variables
        self._dot_x, self._dot_y = None, None
        _dot_picture = Image.open(os.path.join('assets', 'dot.png'))
        self._dot_width, self._dot_height = _dot_picture.width, _dot_picture.height
        self._dot_image = ImageTk.PhotoImage(_dot_picture)
        self._current_direction = None
        self._dot_id = None
        
        # canvas to place images on
        self._canvas = ctk.CTkCanvas(self, width=self._width, height=self._height)
        self._canvas.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self._generate_dot_position()
        
        # warning message if the user's eyes aren't being seen
        self._warning = self._canvas.create_text(self._width * 0.5, self._height * 0.6, text="", font=ctk.CTkFont(size=40), fill="white")
        
        # the current frame of the camera feed
        self._current_image = None
        
        # facial detection using dlib
        self._eyes_detector = dlib.get_frontal_face_detector()
        self._predictor = dlib.shape_predictor(os.path.join('assets', 'shape_predictor_68_face_landmarks.dat'))
        
        # load camera and start data collection
        self._cam = cv2.VideoCapture(0)
        self._update_camera()
        
    # update camera and display it on canvas
    def _update_camera(self):
        ret, frame = self._cam.read()
        if ret:
            # crop the image
            image_crop = self._process_image(cv2.flip(frame, 1))
            display_image, correct = image_crop[0], image_crop[1]
            
            self._eyes_seen = correct

            # if the image is valid
            if correct:
                # save current image to variable
                self._current_image = display_image
                
                # put image on screen if it's properly resized
                self._photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)))
                self._canvas.create_image(self._width * 0.5, self._height * 0.3, image=self._photo, anchor=ctk.CENTER)
                
                self._canvas.itemconfig(self._warning, text="")
            else:
                # inform the user their eyes aren't being seen
                self._canvas.itemconfig(self._warning, text="Eyes are not visible!")
        
        self.after(10, self._update_camera)
    
    # process the image similar to our neural network
    def _process_image(self, image):
        # grayscale image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # if a face is detected
        faces = self._eyes_detector(gray)
        if len(faces) > 0:
            landmarks = self._predictor(gray, faces[0])
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
            
            # get separate images for each eye
            # [start_y:end_y, start_x:end_x]
            left_eye_region = gray[left_eye[1]:left_eye[3], left_eye[0]:left_eye[2]]
            right_eye_region = gray[right_eye[1]:right_eye[3], right_eye[0]:right_eye[2]]
            
            # put eyes into template similar to our training data
            template = self._eye_template(left_eye_region, right_eye_region)
            
            # return resized image and true indicating it can be used for input in our network
            return (cv2.resize(template, (190, 80)), True)
        
        # if no faces are found return original image and false
        return (image, False)
    
    def _eye_template(self, left_eye, right_eye):
        # composite image height and width
        height = max(left_eye.shape[0], right_eye.shape[0])
        width = left_eye.shape[1] + right_eye.shape[1]

        # create a blank image to put data into
        composite_image = np.zeros((height, width), dtype=np.uint8)

        # put left and right eyes in the image side by side
        composite_image[:left_eye.shape[0], :left_eye.shape[1]] = left_eye
        composite_image[:right_eye.shape[0], left_eye.shape[1]:] = right_eye

        # return the composite image
        return composite_image
    
    # takes a picture and saves it to 'images'
    def _take_picture(self, event):
        #only take a picture if the eyes are seen
        if self._eyes_seen:
            # the format for storing the images
            self._img_counter += 1
            img_name = None
            if self._current_direction == "north":
                self._n_counter += 1
                img_name = f'north{self._n_counter}.png'
            elif self._current_direction == "north west":
                self._nw_counter += 1
                img_name = f'northwest{self._nw_counter}.png'
            elif self._current_direction == "north east":
                self._ne_counter += 1
                img_name = f'northeast{self._ne_counter}.png'
            elif self._current_direction == "west":
                self._w_counter += 1
                img_name = f'west{self._w_counter}.png'
            elif self._current_direction == "east":
                self._e_counter += 1
                img_name = f'east{self._e_counter}.png'
            elif self._current_direction == "south west":
                self._sw_counter += 1
                img_name = f'southwest{self._sw_counter}.png'
            elif self._current_direction == "south east":
                self._se_counter += 1
                img_name = f'southeast{self._se_counter}.png'
            elif self._current_direction == "south":
                self._s_counter += 1
                img_name = f'south{self._s_counter}.png'
            elif self._current_direction == "center":
                self._c_counter += 1
                img_name = f'center{self._c_counter}.png'
            
            # save cropped picture to 'images' folder
            cv2.imwrite(os.path.join('images', 'g-crop_' + img_name), self._current_image)
            
            # put dot in new place and delete old dot
            self._canvas.delete(self._dot_id)
            
            # if 100 images have been taken      
            if self._img_counter == NUM_OF_IMAGES:
                self._leave_screen()
            else:
                self._generate_dot_position()
        
    # generates a place on the screen to place the dot.
    def _generate_dot_position(self):
        dir = rand.randint(0, 8)
        if dir == 0: #north west
            self._dot_x = 0
            self._dot_y = 0
            self._current_direction = 'north west'
        elif dir == 1: # north
            self._dot_x = (self._width/2) - (self._dot_width/2)
            self._dot_y = 0 
            self._current_direction = 'north'
        elif dir == 2: # north east
            self._dot_x = self._width - self._dot_width
            self._dot_y = 0
            self._current_direction = 'north east'
        elif dir == 3: # west
            self._dot_x = 0
            self._dot_y = (self._height/2) - (self._dot_height/2)
            self._current_direction = 'west'
        elif dir == 4: # center
            self._dot_x = (self._width/2) - (self._dot_width/2)
            self._dot_y = (self._height/2) - (self._dot_height/2)
            self._current_direction = 'center'
        elif dir == 5: # east
            self._dot_x = self._width - self._dot_width
            self._dot_y = (self._height/2) - (self._dot_height/2)
            self._current_direction = 'east'
        elif dir == 6: # south west
            self._dot_x = 0
            self._dot_y = self._height - self._dot_height
            self._current_direction = 'south west'
        elif dir == 7: # south
            self._dot_x = (self._width/2) - (self._dot_width/2)
            self._dot_y = self._height - self._dot_height
            self._current_direction = 'south'
        elif dir == 8: # south east
            self._dot_x = self._width - self._dot_width
            self._dot_y = self._height - self._dot_height
            self._current_direction = 'south east'
        
        self._dot_id = self._canvas.create_image(self._dot_x, self._dot_y, image=self._dot_image, anchor=ctk.NW)
    
    # close camera and go to next screen
    def _leave_screen(self):
        self._cam.release()
        self.master.unbind("<Key-Space>")
        self._screen_changer('EndScreen')