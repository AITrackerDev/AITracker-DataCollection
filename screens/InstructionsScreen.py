import customtkinter as ctk

class InstructionsScreen(ctk.CTkFrame):
    '''
    Inform user how to use the application.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer
        
        _instructions_label = ctk.CTkLabel(self, text="After clicking continue, the app will generate a dot in a random location on the screen. While looking at it, press the space bar to take a picture. Please be sure to keep your head still while collecting data. The app will inform you if your eyes cannot be seen, but please be sure that the image of your eyes is actually your eyes. This process will repeat 100 times, and can take 5-10 minutes.")
        _instructions_label.configure(wraplength=500)
        _instructions_button = ctk.CTkButton(self, text="Continue", command=lambda: self._screen_changer('DataScreen'))

        _instructions_label.place(relx=.5, rely=0.45, anchor=ctk.CENTER)
        _instructions_button.place(relx=.5, rely=0.9, anchor=ctk.CENTER)