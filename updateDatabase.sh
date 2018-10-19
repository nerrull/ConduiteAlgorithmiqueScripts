#!/usr/bin/env bash

git pull
cp ./database/database.h5 /home/nuc/Documents/dataStore/database.h5
python2 getHapVideoLengths.py
