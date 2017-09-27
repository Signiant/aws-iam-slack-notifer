#!/bin/bash

echo "Creating dist folder"
mkdir -p dist
echo "Copying lambda code into dist folder"
cp -f lambda/iam-notify-slack.py ./dist/iam-notify-slack.py
cd dist
echo "Creating lambda zip"
zip -r iam-notify-slack .
cd ..
echo "DONE"

