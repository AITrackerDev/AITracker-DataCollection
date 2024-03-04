#!/bin/sh

pyinstaller \
  --name 'AITracker-DataCollection' \
  --onefile --windowed \
  --add-data='./assets/dot.png':'./assets/dot.png' \
  --add-data='./assets/haarcascade_eye.xml':'./assets/haarcascade_eye.xml' \
  --add-data='./assets/shape_predictor_68_face_landmarks.dat':'./assets/shape_predictor_68_face_landmarks.dat' \
  DataCollection.py

test -f Application-Installer.dmg && rm Application-Installer.dmg
create-dmg \
  --volname "AITracker-DataCollection" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "AITracker-DataCollection.app" 175 120 \
  --hide-extension "AITracker-DataCollection.app" \
  --app-drop-link 425 120 \
  "AITracker-DataCollection.dmg" \
  "./dist"