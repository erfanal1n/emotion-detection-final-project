# Emotion Detection

A small Flask application that uses IBM Watson NLP to detect anger, disgust, fear, joy, and sadness in English text.

## Setup

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
python server.py
```

Open `http://127.0.0.1:5000`, enter a sentence, and select **Analyze text**. The Watson NLP endpoint needs an internet connection.

## Verify

```powershell
python -m unittest discover -v
python -m pylint server.py EmotionDetection test_emotion_detection.py
```

The detector is in `EmotionDetection/emotion_detection.py`. The Flask page and request handling are in `server.py`.

Starter repository: [IBM Developer Skills Network final project](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai).
