def detect_emotion(text):
    text = text.lower()

    if any(word in text for word in ["ভালোবাসি", "মিস", "প্রেম", "ভালবাসা"]):
        return "love"

    elif any(word in text for word in ["কষ্ট", "ব্যথা", "অভিমান", "চোখের জল"]):
        return "sad"

    elif any(word in text for word in ["হাসি", "আনন্দ", "মজা", "চমৎকার"]):
        return "happy"

    elif any(word in text for word in ["রাগ", "ঘৃণা", "মেজাজ", "বোকা"]):
        return "angry"

    else:
        return "neutral"
