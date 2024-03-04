#!/bin/sh

pyinstaller AITracker-DataCollection.spec

directory=$(PWD)
cd dist
rm AITracker-DataCollection
cd "$directory"

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