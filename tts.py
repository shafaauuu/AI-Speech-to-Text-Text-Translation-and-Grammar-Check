from gtts import gTTS
import os

def TTS(text, lang):
    # Create a gTTS object
    tts = gTTS(text=text, lang=lang, slow=False)

    # Save the speech to a file
    tts.save("output.mp3")