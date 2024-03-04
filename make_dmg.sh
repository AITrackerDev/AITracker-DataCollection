#!/bin/sh

# compile python script from spec file
pyinstaller AITracker-DataCollection.spec

# remove compiled binary
directory=$(PWD)
cd dist
rm AITracker-DataCollection

# create assets folder in the compiled app
cd "AITracker-DataCollection.app/Contents/MacOS"
mkdir assets
cd "$directory"

# copy assets into the compiled app
cp -R "$directory"/assets/. "dist/AITracker-DataCollection.app/Contents/MacOS/assets/"

# create a macOS dmg
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