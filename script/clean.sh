#!/bin/bash

chmod 644 .gitignore .pre-commit-config.yml .travis.yml
chmod 644 Dockerfile LICENSE Makefile MANIFEST.in README.md
chmod 644 requirements.txt setup.cfg action.py setup.py

find gerritaction tests -name "*.py" -exec chmod 644 {} \;
find gerritaction tests -name "*.yml" -exec chmod 644 {} \;
find . -name "*.pyc" ! -path "*.venv*" -exec rm -rf {} \;
find . -name "*.sh" ! -path "*.venv*" -exec chmod 755 {} \;
find . -name "__pycache__" ! -path "*.venv*" -exec rm -rf {} \;
