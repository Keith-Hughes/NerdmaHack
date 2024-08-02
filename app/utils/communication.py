
from flask import current_app
import requests
import smtplib, ssl
from email.message import EmailMessage
import json


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
        'file': (file_path, open(file_path, 'rb'), 'audio/mpeg')
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
            },
            'context': {
                'message_id': origin_message['id']
        }
        }

        response = requests.post(url, headers=headers, json=json)
        print (response)
        return response
    except:
        return send_whatsapp_message(origin_message, "unable to process")

def send_whatsapp_document_message(origin_message, file_path):

    PHONE_NUMBER_ID = current_app.config.get("PHONE_NUMBER_ID")
    ACCESS_TOKEN = current_app.config.get("WHATSAPP_ACCESS_TOKEN")

    headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    upload_url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/media"

    files = {
        'file': (file_path, open(file_path, 'rb'), 'application/pdf')
    }

    upload_json = {
        'messaging_product': 'whatsapp',
        'type': 'application/pdf'
    }
    try:
        response= requests.post(upload_url, headers=headers, files=files, data=upload_json)
        print("Document uploaded")

        url= f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
        
        json={
            'messaging_product': 'whatsapp',
            'to': origin_message['from'],
            'type': "document",
            "document": {
                "id": response.json()['id'],
                "filename": file_path
            },
            'context': {
                'message_id': origin_message['id']
        }
        }
        print
        response = requests.post(url, headers=headers, json=json)
        print (response)
        return response
    except:
        return send_whatsapp_message(origin_message, "unable to process")

def send_email_message(subject, body, to_email):
    context = ssl.create_default_context()
    port = current_app.config.get('MAIL_PORT')
    password = current_app.config.get('MAIL_PASSWORD')
    user = current_app.config.get('MAIL_USERNAME')
    server = current_app.config.get('MAIL_SERVER')
    from_email = "solutions@stocktally.co.za"

    # Create the email message
    print("Creating")
    msg = EmailMessage()

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL(server, port, context=context) as server:
            print('Sending message...')
            login_response = server.login(user, password)
            print(login_response)
            result = server.send_message(msg)
            response = {"success": True, "message": "Email sent successfully to "+ to_email}
    except Exception as e:
        response = {"success": False, "message": "Could not deliver the email", "error": str(e)}   

    return json.dumps(response)

def send_email_file(file_path, to_email):

    return True

