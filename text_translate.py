from googletrans import Translator

def translate_text(text, dest):
    translator = Translator()
    translated_text = translator.translate(text, dest, src="en").text
    
    return translated_text