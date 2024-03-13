import customtkinter as ctk
import numpy as np
import datetime
import os
import h5py
import cv2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

class EndScreen(ctk.CTkFrame):
    '''
    Informs user app is safe to close.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer
        
        h5path = self.createH5()
        #self.sendEmail(h5path)
        
        finished_text = ctk.CTkLabel(self, text="Thank you for helping us collect data for our neural network! If you can see this message, the application is safe to close.")
        finished_button = ctk.CTkButton(self, text="Quit", command=lambda: root.quit())
        finished_text.place(relx=.5, rely=.5, anchor=ctk.CENTER)
        finished_button.place(relx=.5, rely=.75, anchor=ctk.CENTER)
        
        #os.remove(h5path)
    
    def createH5(self):
        # images and labels for h5 file
        images = []
        labels = []

        # loop through all images
        for filename in os.listdir('images'):
            if filename.startswith('g-') and filename.endswith('.png'):
                # read in the image without adding other color channels
                image = cv2.imread(os.path.join('images', filename), cv2.IMREAD_UNCHANGED)
                images.append(image)
                labels.append(os.path.splitext(filename)[0])

        # Convert the lists to NumPy arrays
        images = np.array(images)
        labels = np.array(labels, dtype='S')

        # Format the date and time to create a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create a file name using the timestamp
        h5path = f"image_collection{timestamp}.h5"
        h5f = h5py.File(h5path, 'w')

        # Create datasets for resized images and labels
        h5f.create_dataset('images', data=images)
        h5f.create_dataset('labels', data=labels)

        # Close the HDF5 file
        h5f.close()

        # Return path of h5 file
        return h5path
    
    def sendEmail(self, path):
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