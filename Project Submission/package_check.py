"""Check the package offline."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from EmotionDetection.emotion_detection import emotion_detector

scores = {
    "anger": 0.9,
    "disgust": 0.02,
    "fear": 0.02,
    "joy": 0.03,
    "sadness": 0.03,
}
response = Mock(status_code=200)
response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}

print("from EmotionDetection.emotion_detection import emotion_detector")
with patch(
    "EmotionDetection.emotion_detection.requests.post",
    return_value=response,
):
    print(emotion_detector("I am really mad about this"))
print("EmotionDetection is a valid package")
