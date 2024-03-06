import os
import shutil
import platform
import ctypes
import sys
import customtkinter as ctk
from screens.ConsentScreen import ConsentScreen
from screens.InstructionsScreen import InstructionsScreen
from screens.DataScreen import DataScreen
from screens.EndScreen import EndScreen

class AITrackerDataCollection(ctk.CTk):
    '''
    Create a new app window, set the attributes, and load the consent screen.
    '''
    
    def __init__(self):
        super().__init__()

        # window setup
        self.title('AITracker Data Collection')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.geometry('1080x720')
        self.attributes('-topmost', 1)
        self.update()
        self.attributes('-topmost', 0)
        self.wm_attributes('-fullscreen', True)
        self._current_screen = None
        
        # screen references to load them when requested
        self._screens = {
            'ConsentScreen':ConsentScreen,
            'InstructionsScreen':InstructionsScreen,
            'DataScreen':DataScreen,
            'EndScreen':EndScreen
        }
        
        # load consent screen
        self.show_screen('ConsentScreen')

    def show_screen(self, screen_name):
        '''
        Loads in and displays a new screen as requested.
        '''
        
        # if the current screen exists
        if self._current_screen:
            self._current_screen.destroy()
        
        # load new screen
        screen_class = self._screens[screen_name]
        self._current_screen = screen_class(self, self.show_screen)
        self._current_screen.pack()

if __name__ == '__main__':
    # platform specific fixes
    if platform.system() == 'Windows':
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    
    # change directory to where this file is being ran so assets can be loaded after compiling
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
       
    # create directory for images
    if not os.path.isdir("images"):
        os.mkdir("images")
    else:
        shutil.rmtree("images")
        os.mkdir("images")

    app = AITrackerDataCollection()
    app.mainloop()
    
    # removes images directory to prevent them from being included on the next run of the application
    shutil.rmtree("images")