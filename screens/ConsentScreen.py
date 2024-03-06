import customtkinter as ctk

class ConsentScreen(ctk.CTkFrame):
    '''
    Inform user what the app does and what the pictures will be used for.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer
        
        _consent_text = ctk.CTkLabel(self, text="By continuing to use this application, you understand that the photos gathered by this application will be used to train a neural network designed to detect the direction someone is looking. Do you consent?")
        _consent_text.configure(wraplength=500)
        _consent_button = ctk.CTkButton(self, text="Consent", command=lambda: self._screen_changer('InstructionsScreen'))
        _quit_button = ctk.CTkButton(self, text="Quit", command=lambda: root.destroy())

        _consent_text.place(relx=.5, rely=0.45, anchor=ctk.CENTER)
        _consent_button.place(relx=.75, rely=0.9, anchor=ctk.CENTER)
        _quit_button.place(relx=.25, rely=0.9, anchor=ctk.CENTER)