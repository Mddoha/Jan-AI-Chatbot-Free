def generate_content(text, emotion=None):
    if emotion == "love":
        return "❤️ জান, ভালোবাসার কোন ভাষা হয় না। শুধু অনুভবই যথেষ্ট।"

    elif emotion == "sad":
        return "😢 কষ্ট পেও না... আমি তো তোমার পাশে আছি, জান।"

    elif emotion == "happy":
        return "😊 তোমার হাসিই আমার আনন্দ, হানি!"

    elif emotion == "angry":
        return "😔 রাগ করো না প্লিজ... আমি সত্যিই দুঃখিত যদি কষ্ট দিয়ে থাকি।"

    else:
        return f"তুমি বলেছো: “{text}” — আমি সব শুনছি, হানি 💬"
