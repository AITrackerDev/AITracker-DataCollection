from setuptools import setup

APP = ['DataCollection.py']
DATA_FILES = ['assets/shape_predictor_68_face_landmarks.dat', 'assets/dot.png', 'assets/haarcascade_eye.xml']
OPTIONS = {'packages' : ['Functions.py'], 'argv_emulation': True}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)