#!/bin/sh

# compile python script from spec file
pyinstaller --noconfirm AITracker-DataCollection.spec

# save current directory and remove .app file
directory=$(PWD)
cd dist
rm -R "DataCollection.app/"

# copy assets and quarantine script into the compiled app directory
cp -R "$directory"/assets/. "./AITracker-DataCollection/assets"
cp "$directory/quarantine.sh" "AITracker-DataCollection/"
cp "$directory/Info.plist" "AITracker-DataCollection/"