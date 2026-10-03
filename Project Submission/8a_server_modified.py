"""Flask emotion detection app."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET"])
def detect_emotion():
    """Format emotion scores."""
    text_to_analyse = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyse:
        return "Please enter text to analyze.", 400

    try:
        result = emotion_detector(text_to_analyse)
    except RequestException:
        return "The emotion service is temporarily unavailable.", 502

    if result["dominant_emotion"] is None:
        return "The service could not analyze this text.", 400

    emotions = ", ".join(
        f"'{emotion}': {result[emotion]}"
        for emotion in ("anger", "disgust", "fear", "joy", "sadness")
    )
    return (
        f"For the given statement, the system response is {emotions}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
