# This is the data collection application of our program
# All this does is take a picture and saves it to the folder "data_images"
import customtkinter as ctk
import h5py
import numpy as np

#global height and width variables
WIDTH = 720
HEIGHT = 480
currentFrame = 0

#app window setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry(str(WIDTH) + "x" + str(HEIGHT))
app.title("aiTracker Data Collection")

#frame instantiations
consentFrame = ctk.CTkFrame(master = app, width = WIDTH, height = HEIGHT)
instructionsFrame = ctk.CTkFrame(master = app, width = WIDTH, height = HEIGHT)
dataFrame = ctk.CTkFrame(master = app, width = WIDTH, height = HEIGHT)
endFrame = ctk.CTkFrame(master = app, width = WIDTH, height = HEIGHT)

#strings for the different frames
consentString = "By continuing to use this application, you understand that the photos gathered by this application will be used to train a neural network designed to detect the direction someone is looking. Do you consent?"
instructionsString = "After clicking continue, the app will generate a random dot on the screen. While looking at it, press the space bar once, and a picture will be taken and a new dot will be generated in a new location. This process will repeat approximately 50 times."

#button functions
def loadFrame(destroyFrame, loadFrame):
    #sets the currentFrame variable to the one that's laoded
    global currentFrame
    currentFrame = loadFrame
    #destroys the previous frame and loads the next one
    destroyFrame.destroy()
    loadFrame.pack()

#empty function that activates when the dataFrame is loaded, and when the space button is pressed   
def dataCollectionFunction(event):
    if currentFrame == dataFrame:
        print("Space pressed")
    
#widgets contained in each frame
#consent frame
consentText = ctk.CTkLabel(consentFrame, text = consentString)
consentText.configure(wraplength = 500)
consentButton = ctk.CTkButton(consentFrame, text = "Consent", corner_radius=10, command = lambda: loadFrame(consentFrame, instructionsFrame))
quitButton = ctk.CTkButton(consentFrame, text = "Quit", corner_radius=10, command = lambda: app.destroy())

consentText.place(relx = .5, rely = 0.45, anchor = ctk.CENTER)
consentButton.place(relx = .75, rely = 0.9, anchor = ctk.CENTER)
quitButton.place(relx = .25, rely = 0.9, anchor = ctk.CENTER)

#instructions frame
instructionsLabel = ctk.CTkLabel(instructionsFrame, text = instructionsString)
instructionsLabel.configure(wraplength = 500)
instructionsButton = ctk.CTkButton(instructionsFrame, text = "Continue", corner_radius=10, command = lambda: loadFrame(instructionsFrame, dataFrame))

instructionsLabel.place(relx = .5, rely = 0.45, anchor = ctk.CENTER)
instructionsButton.place(relx = .5, rely = 0.9, anchor = ctk.CENTER)

#data collection frame
app.bind("<Key-space>", dataCollectionFunction)
"""
    camera footage in the screen
    space button captures photo and saves it to data_images
"""

#create example hdf5 file
fileW = h5py.File("example.hdf5", "w")

dataset = fileW.create_dataset("data", shape=(10,), dtype='i')

for i in range(10):
    dataset[i] = i

fileW.close()

#read example hdf5 file after it is created
fileR = h5py.File("example.hdf5", "r")

dataset = fileR["data"]
data = np.array(dataset)

fileR.close()

print("Example Data:")
print(data)

#program finished frame
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

consentFrame.pack()
app.mainloop()