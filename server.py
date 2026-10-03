"""Serve the emotion detector as a Flask web application."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    """Render the detector page."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and format the scores."""
    text = request.args.get("textToAnalyze", "").strip()
    if not text:
        return "Please enter text to analyze.", 400

    try:
        result = emotion_detector(text)
    except RequestException:
        return "The emotion service is temporarily unavailable.", 502

    if result["dominant_emotion"] is None:
        return "The service could not analyze this text.", 400

    score_text = ", ".join(
        f"{emotion} is {result[emotion]:.3f}"
        for emotion in ("anger", "disgust", "fear", "joy", "sadness")
    )
    return (
        f"For the given statement, the system response is: {score_text}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(debug=False)
