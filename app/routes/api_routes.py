from flask import Blueprint, request, jsonify, current_app
import requests
from app.utils import *
import json
import threading


api_bp = Blueprint('api', __name__)


@api_bp.route('/process-text', methods=['POST'])
def process_text():
    ACCESS_TOKEN = current_app.config.get('WHATSAPP_ACCESS_TOKEN')
    data = request.json
    print("Incoming webhook message:", data)

    app = current_app._get_current_object()
    def message_proccessing(data, ACCESS_TOKEN, current_app):
        with current_app.app_context():    
            message = data.get('message')

            if data:

                

                if message and message.get('type') == 'text':
                    print(message)
                    response = determine_crud(message.get('text').get('body'))
                    if response != "AI working":
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

                    print(audio_response)    

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

                                if response != "AI working":
                                    audio_file=text_to_audio(response, audio_id)
                                    send_whatsapp_voice_message(message, audio_file)

    thread = threading.Thread(target=message_proccessing, args=(data, ACCESS_TOKEN, app))
    thread.start()            
    

    return jsonify({'status': 'success', 'message': 'message received'}), 200

