from flask import Flask, request, render_template, jsonify
import os
from utils.ai_utils import *
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import requests
import json

load_dotenv('.env')
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
PORT = 5000
ACCESS_TOKEN= os.getenv("ACCESS_TOKEN")

app = Flask(__name__)
client = OpenAI()
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def transcribe_audio(audio_path):
    response = {"message": "",
                "is_success": True,
                }
    audio_file = Path(audio_path)
    try:
        transcription = client.audio.transcriptions.create(
			model="whisper-1", 
			file=audio_file
		)
        response['message'] = transcription.text
    except Exception as e:
        response['is_success'] = False
        response['message'] = str(e)
    finally:
        return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'voiceMessage' not in request.files:
        return 'No file part', 400
    file = request.files['voiceMessage']

    if file.filename == '':
        return 'No selected file', 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    transcription = transcribe_audio(file_path)
    
    if not transcription['is_success']:
        return f'Transcription Failed: {transcription['message']}', 400
    
    return f'Transcription: {transcription}', 200

def send_whatsapp_message(origin_message, reply):
    url= f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    json={
        'messaging_product': 'whatsapp',
        'to': origin_message['from'],
        'text': {'body': reply},
        'context': {
            'message_id': origin_message['id']
        }
    }

    response = requests.post(url, headers=headers, json=json)
    print (response)
    return response


@app.route('/process-text', methods=['POST'])
def process_text():

    data = request.json
    print("Incoming webhook message:", data)

    message = data.get('message')
    print(message)

    if data:

        if message and message.get('type') == 'text':
            print(message)
            response = determine_crud(message.get('text').get('body'))
            send_whatsapp_message(message, response)
            return jsonify({'status': 'success', 'message': 'Reply sent successfully'}), 200

        elif message and message.get('type') == 'audio':
            print('audio received', message)
            audio_id = message.get('audio').get('id')
            audio_response = requests.get(
                f'https://graph.facebook.com/v20.0/{audio_id}',
                headers={
                    'Authorization': f'Bearer {ACCESS_TOKEN}',
                }
            )    

            if (audio_response.status_code == 200):
                audio_data = json.loads(audio_response.content)
                audio_url = audio_data.get('url')
                audio_content_response = requests.get(
                    audio_url,
                    headers={
                        'Authorization': f'Bearer {ACCESS_TOKEN}',
                    }
                )
                
                if audio_content_response.status_code == 200:
                    
                    audio_content = audio_content_response.content
                    audio_filename = f"audio_{audio_id}.ogg"

                    with open(audio_filename, 'wb') as audio_file:
                        audio_file.write(audio_content)
                    
                    print(f"Audio file saved as {audio_filename}")
                
                    transcribed = transcribe_audio(audio_filename)
                    print('transcribed audio', transcribed)
                    if(transcribed['is_success']):
                        response=determine_crud(transcribed['message'])
                        send_whatsapp_message(message, response)
            return jsonify({'status': 'success', 'message': 'message'}), 200

    return jsonify({'status': 'success', 'message': 'No text message found'}), 200

if __name__ == '__main__':
    app.run(debug=True)
    # send_whatsapp_message("+27733131122")

