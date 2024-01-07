# aiTracker Data Collection Application

## What is this?

This program is our application to collect our training data for our neural network. The premise of our network is to determine which direction the user is looking only using a standard webcam. As the data we need to collect is fairly specific, this application will assist us in getting the necessary data we need, as well as preprocess it for our needs.

## Requirements
### Windows
If you are on Windows, the best way to install Python is by visiting [this website](https://www.python.org/downloads/windows/). The package manager pip comes installed automatically if downloaded from this website.

### MacOS
As for MacOS, the easiest way to install Python is through Homebrew, which is a package manager for command line utilities and applications. The command to install it is

 `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"`. 
 
 Once installed, run the command `brew install python3` and Python will be installed. Python should now be setup properly.

### Setup
This project relies on a few different libraries installed via pip. The following commands will help set everything up quick and easy. We're going to create a virtual environment, activate it, and download all of the necessary requirements for the project with these 3 commands.

Create the virtual environment:
`python3.8 -m venv env`

Activate the virtual environment:
`source env/bin/activate`

Install the necessary versions of the required packages:
`pip install -r requirements.txt`

On Windows, there may be an error regarding installing dlib. To fix this, [this article](https://medium.com/analytics-vidhya/how-to-install-dlib-library-for-python-in-windows-10-57348ba1117f) does a good job in explaining what goes wrong and how to fix it.

## How to run

Run the command while in the directory of the project. The application will guide you from there.

`python3 DataCollection.py`

## Known bugs
* On MacOS, the buttons in fullscreen are a little finicky, and may not respond immediately. This is a Tkinter problem, and not a bug we are in control of fixing. To remedy this, click in the app window a few times, or force click in the app window/button in order to get it to register.