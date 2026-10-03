# Final Project: Emotion Detector

This repository contains an emotion detection web application built with Python, Flask, and the IBM Watson NLP emotion model. It predicts anger, disgust, fear, joy, and sadness from English text.

## Project details

- Project: Emotion Detector
- Course project: Final Project – Emotion Detector
- Public repository: https://github.com/erfanal1n/emotion-detection-final-project
- Original starter: IBM Skills Network repository at https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai
- Application package: EmotionDetection
- Application module: EmotionDetection/emotion_detection.py
- Flask server: server.py

## Setup

Install dependencies with: python -m pip install -r requirements.txt

## Run

Start the web app with: python server.py

Open http://127.0.0.1:5000, enter a sentence, and select Analyze text. The Watson NLP endpoint needs an internet connection.

## Verify

Run python -m unittest discover -v and python -m pylint server.py EmotionDetection test_emotion_detection.py.

The Project Submission folder contains task code extracts, command outputs, and screenshots used for the course assignment. See Project Submission/README.md for the answer map. Mocked responses are marked in the evidence files.
