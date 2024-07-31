
from flask import current_app
import requests


def send_whatsapp_message(origin_message, reply):

    PHONE_NUMBER_ID = current_app.config.get("PHONE_NUMBER_ID")
    ACCESS_TOKEN = current_app.config.get("WHATSAPP_ACCESS_TOKEN")

    url= f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
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

def send_whatsapp_voice_message(origin_message, file_path):

    PHONE_NUMBER_ID = current_app.config.get("PHONE_NUMBER_ID")
    ACCESS_TOKEN = current_app.config.get("WHATSAPP_ACCESS_TOKEN")

    headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    upload_url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/media"

    files = {
        'file': (file_path, open(file_path, 'rb'), 'audio/mp3')
    }

    upload_json = {
        'messaging_product': 'whatsapp',
        'type': 'audio/mpeg'
    }
    try:
        response= requests.post(upload_url, headers=headers, files=files, data=upload_json)
        print(response.text)
        print(response._content)

        url= f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
        
        json={
            'messaging_product': 'whatsapp',
            'to': origin_message['from'],
            'type': "audio",
            'audio': {
                'id': response.json()['id']
            }
        }

        response = requests.post(url, headers=headers, json=json)
        print (response)
        return response
    except:
        return send_whatsapp_message(origin_message, "unable to process")

def send_email_message(message, to_email):

    return True

def send_email_file(file_path, to_email):

    return True