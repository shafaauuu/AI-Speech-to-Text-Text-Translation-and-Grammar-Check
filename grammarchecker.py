import language_tool_python


def grammar_check_speech(text):
    
    if not text:
        return "No speech provided."

    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = tool.correct(text)

    return corrected_text

# print(grammar_check_speech("I is testng grammar tool using python. It does not costt anythng."))