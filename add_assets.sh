#!/bin/sh

# compile python script from spec file
pyinstaller AITracker-DataCollection.spec

directory=$(PWD)
cd dist

# create assets folder in the compiled app
cd "AITracker-DataCollection"
mkdir assets
cd "$directory"

# copy assets into the compiled app directory
cp -R "$directory"/assets/. "AITracker-DataCollection"