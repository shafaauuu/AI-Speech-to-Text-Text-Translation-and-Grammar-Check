# an object of WSGI application 
import os

from tts import TTS
from predict import STT
from grammarchecker import grammar_check_speech
from text_translate import translate_text

from flask import Flask, render_template, request, jsonify, send_file
app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def index(): 
    return render_template("index.html")

@app.route("/stt-predict", methods=["POST"])
def stt_predict():
    
    if 'input_audio' not in request.files:
        return 'No file part'

    file = request.files['input_audio']
    
    file_path = ""
    
    if file:
        # Save the file to a directory
        filename = file.filename
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
    
    stt = STT()
    
    return stt.predict(file_path)

@app.route("/grammar-check", methods=["POST"])
def grammar_check():
    
    text = request.data.decode("utf-8")
    
    checked = grammar_check_speech(text)
    
    return checked
  
@app.route("/translate", methods=["POST"])
def translate():
    json_data = request.get_json()
    
    text = json_data.get("text", "There is no message")
    dest = json_data.get("dest", "en")
    
    result = translate_text(text, dest)
    
    return result

@app.route('/tts', methods=['POST'])
def text_to_speech():
    json_data = request.get_json()
        
    text = json_data.get('text')  # Extract 'text' from JSON data
    language = json_data.get('dest')

    TTS(text, language)
    
    return send_file("output.mp3", as_attachment=True)

if __name__=='__main__': 
   app.run() 