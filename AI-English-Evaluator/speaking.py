import speech_recognition as sr
from writing import evaluate_writing

def evaluate_speaking(audio_file):

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio)

    except Exception:
        transcript = ""

    if transcript == "":
        return {
            "transcript": "",
            "overall_score": 0,
            "grammar": "Transcript gagal dibuat.",
            "vocabulary": "-",
            "suggestion": "Coba upload audio yang lebih jelas."
        }

    result = evaluate_writing(transcript)

    result["transcript"] = transcript

    return result