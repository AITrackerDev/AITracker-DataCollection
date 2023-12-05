# aiTracker Data Collection Application

## What is this?

This program is our application to collect our training data for our neural network. The premise of our network is to determine which direction the user is looking only using a standard webcam. As the data we need to collect is fairly specific, this application will assist us in getting the necessary data we need, as well as preprocess it.

## Requirements
### Windows
If you are on Windows, the best way to install Python is by visiting [this website](https://www.python.org/downloads/windows/). pip comes installed automatically if downloaded from this website.

### MacOS
As for MacOS, the easiest way to install Python is through Homebrew. The command to install it can be found [here](https://brew.sh/). Once installed, run the command `brew install python3` and Python will be installed. pip comes installed automatically if installed via Homebrew.

### Libraries and Packages
This project relies on a few different libraries installed via pip. To make the process easier, the following command will take care of all the necessary installations at once.

`pip install numpy opencv-python h5py matplotlib pillow tk dlib`

## How to run

Run the command while in the directory of the project.

`python3 DataCollection.py`

## Known bugs
* On MacOS, the buttons in fullscreen are a little finicky, and may not respond immediately. This is a TKinter problem, and not a bug we are in control of fixing. To remedy this, click in the app window a few times, or force click in the app window/button in order to get it to register.