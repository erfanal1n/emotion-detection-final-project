"""Check the raw module offline."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emotion_detection import emotion_detector

scores = {
    "anger": 0.9,
    "disgust": 0.02,
    "fear": 0.02,
    "joy": 0.03,
    "sadness": 0.03,
}
response = Mock()
response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}

print("from emotion_detection import emotion_detector")
with patch("emotion_detection.requests.post", return_value=response):
    print(emotion_detector("I am really mad about this"))
