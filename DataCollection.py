# This is the data collection application of our program
# All this does is take a picture and saves it to the folder "data_images"
import customtkinter as ctk

#setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("720x480")
app.title("aiTracker Data Collection")

consentString = "By continuing to use this application, you understand that the photos gathered by this application will be used to train a neural network designed to detect the direction someone is looking. Do you consent?"

#button functions
def quitApp():
    app.destroy()
    
def consent():
    #do something to continue to data collection
    print("Consent")

#widget creation and placing
consentText = ctk.CTkLabel(app, text = consentString)
consentText.configure(wraplength = 500)
consentButton = ctk.CTkButton(app, text = "Consent", corner_radius=10, command = consent)
quitButton = ctk.CTkButton(app, text = "Quit", corner_radius=10, command = quitApp)

consentText.place(relx = .5, rely = 0.45, anchor=ctk.CENTER)
consentButton.place(relx = .75, rely = 0.9, anchor=ctk.CENTER)
quitButton.place(relx = .25, rely = 0.9, anchor=ctk.CENTER)

app.mainloop()