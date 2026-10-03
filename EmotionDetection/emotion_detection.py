"""Detect emotions with the Watson NLP service."""

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text):
    """Return emotion scores and the strongest emotion."""
    response = requests.post(
        API_URL,
        headers={"grpc-metadata-mm-model-id": MODEL_ID},
        json={"raw_document": {"text": text}},
        timeout=15,
    )

    if response.status_code == 400:
        return {**dict.fromkeys(EMOTIONS), "dominant_emotion": None}

    response.raise_for_status()
    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(EMOTIONS, key=result.__getitem__)
    return result
