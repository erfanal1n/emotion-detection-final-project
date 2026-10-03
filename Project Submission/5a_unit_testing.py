"""Tests for the emotion app."""

import unittest
from unittest.mock import Mock, patch

from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import EMOTIONS, emotion_detector
from server import app


def emotion_response(dominant_emotion):
    """Build a Watson response."""
    scores = dict.fromkeys(EMOTIONS, 0.05)
    scores[dominant_emotion] = 0.8
    response = Mock(status_code=200)
    response.json.return_value = {"emotionPredictions": [{"emotion": scores}]}
    return response


class EmotionDetectorTests(unittest.TestCase):
    """Check Watson predictions."""

    def test_course_examples(self):
        """Check all five emotions."""
        examples = (
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        )
        responses = [emotion_response(expected) for _, expected in examples]

        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            side_effect=responses,
        ):
            for text_to_analyse, expected in examples:
                result = emotion_detector(text_to_analyse)
                self.assertEqual(result["dominant_emotion"], expected)

    def test_returns_none_for_bad_request(self):
        """Handle HTTP 400."""
        response = Mock(status_code=400)

        with patch(
            "EmotionDetection.emotion_detection.requests.post",
            return_value=response,
        ):
            result = emotion_detector("")

        expected = {**dict.fromkeys(EMOTIONS), "dominant_emotion": None}
        self.assertEqual(result, expected)


class EmotionRouteTests(unittest.TestCase):
    """Check Flask routes."""

    def setUp(self):
        self.client = app.test_client()

    def test_home_page_loads(self):
        """Load the home page."""
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detection", response.data)

    def test_blank_text_returns_error(self):
        """Reject blank text."""
        response = self.client.get("/emotionDetector?textToAnalyze=%20%20")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_data(as_text=True),
            "Please enter text to analyze.",
        )

    def test_route_formats_scores(self):
        """Format all scores."""
        result = {
            "anger": 0.8,
            "disgust": 0.05,
            "fear": 0.05,
            "joy": 0.05,
            "sadness": 0.05,
            "dominant_emotion": "anger",
        }
        with patch("server.emotion_detector", return_value=result):
            response = self.client.get(
                "/emotionDetector?textToAnalyze=I%20am%20really%20mad"
            )

        self.assertEqual(response.status_code, 200)
        body = response.get_data(as_text=True)
        self.assertIn("'anger': 0.8", body)
        self.assertIn("dominant emotion is anger", body)

    def test_service_error_returns_message(self):
        """Handle Watson errors."""
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
