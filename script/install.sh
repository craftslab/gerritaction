#!/bin/bash

pip install -U pyinstaller
pip install -U pywin32
pip install -Ur requirements.txt

pyinstaller --clean --name gerritaction --upx-dir /usr/bin -F action.py
