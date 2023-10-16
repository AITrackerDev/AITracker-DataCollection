# This is the data collection application of our program
# All this does is take a picture and saves it to the folder "data_images"
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("720x480")
app.title("aiTracker Data Collection")

app.mainloop()