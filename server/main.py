import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import openai
import json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'mpeg', 'mpga',
                      'm4a', 'wav', 'webm'}

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True

openai.organization = openai.api_key = os.getenv('ORGANIZATION')
openai.api_key = os.getenv('OPENAI_API_KEY')


@app.route('/', methods=['POST'])
@cross_origin()
def upload_file():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Format not valid.'})

    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    transcripted_number = transcript_number(filename)
    return jsonify(transcripted_number)


def allowed_file(filename):
    return any(map(lambda extention: filename.endswith(extention), ALLOWED_EXTENSIONS))


def transcript_number(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'rb') as audiofile:
        transcript = openai.Audio.transcribe("whisper-1", audiofile)
    data = json.loads(str(transcript))
    text = data['text']
    
    try:
        float(text)
        print('ok')
        return { 'text': text }
    except ValueError:
        print('erro')
        return { 'error': 'Number not found' }

if __name__ == '__main__':
    load_dotenv()
    app.run()
