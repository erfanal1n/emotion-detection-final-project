"""Check formatted output."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from EmotionDetection.emotion_detection import emotion_detector

scores = {
    "anger": 0.05,
    "disgust": 0.02,
    "fear": 0.08,
    "joy": 0.81,
    "sadness": 0.04,
}
response = Mock(status_code=200)
response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}

with patch(
    "EmotionDetection.emotion_detection.requests.post",
    return_value=response,
):
    print(emotion_detector("I am happy with the result."))
