"""Tests for the emotion detector and Flask routes."""

import unittest
from unittest.mock import Mock, patch

from requests.exceptions import RequestException

from EmotionDetection import emotion_detector
from EmotionDetection.emotion_detection import API_URL, EMOTIONS, MODEL_ID
from server import app


class EmotionDetectorTests(unittest.TestCase):
    """Check Watson response handling."""

    def test_formats_scores_and_dominant_emotion(self):
        """Check formatted scores."""
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
            "EmotionDetection.emotion_detection.requests.post", return_value=response
        ) as post:
            result = emotion_detector("I am happy with the result.")

        self.assertEqual(result, {**scores, "dominant_emotion": "joy"})
        post.assert_called_once_with(
            API_URL,
            headers={"grpc-metadata-mm-model-id": MODEL_ID},
            json={"raw_document": {"text": "I am happy with the result."}},
            timeout=15,
        )

    def test_returns_empty_scores_for_bad_request(self):
        """Handle HTTP 400."""
        response = Mock(status_code=400)

        with patch(
            "EmotionDetection.emotion_detection.requests.post", return_value=response
        ):
            result = emotion_detector("")

        self.assertEqual(result, {**dict.fromkeys(EMOTIONS), "dominant_emotion": None})


class EmotionRouteTests(unittest.TestCase):
    """Check the browser-facing routes."""

    def setUp(self):
        self.client = app.test_client()

    def test_home_page_loads(self):
        """Load the home page."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detection", response.data)

    def test_blank_text_returns_helpful_error(self):
        """Reject blank input."""
        response = self.client.get("/emotionDetector?textToAnalyze=%20%20")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True), "Please enter text to analyze.")

    def test_route_formats_detection_result(self):
        """Format the route result."""
        result = {
            "anger": 0.05,
            "disgust": 0.02,
            "fear": 0.08,
            "joy": 0.81,
            "sadness": 0.04,
            "dominant_emotion": "joy",
        }
        with patch("server.emotion_detector", return_value=result):
            response = self.client.get(
                "/emotionDetector?textToAnalyze=I%20feel%20great"
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("dominant emotion is joy", response.get_data(as_text=True))

    def test_service_failure_returns_helpful_error(self):
        """Handle service timeouts."""
        with patch("server.emotion_detector", side_effect=RequestException):
            response = self.client.get(
                "/emotionDetector?textToAnalyze=I%20feel%20great"
            )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_data(as_text=True),
            "The emotion service is temporarily unavailable.",
        )


if __name__ == "__main__":
    unittest.main()
