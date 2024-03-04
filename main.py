from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAKKS0Ly7z8BOxNS6LTysRdE4f7EToZBrIUJj9POeKpqrkKfMAQb9KIOOKCidQ3hBgXzt5J3R9NUKpphPa4isdsj3ZAZA9TT5DIZAhFkrHKABe10MLjnh6LYRYFuKigdOnCDlD2f1N29fTeUnOSCCAZAUNzdvKqmnWXuTgKjYy4qHOmotJmJWUAZCtyl8bc9LRZAXUSBzKqakSC42fR'
VERIFY_TOKEN = 'M0nT0k3nD3V3r1f1c@t10n'
APP_SECRET = '22af998db201e29025b0a836e88df1b9'

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.verify_token') == VERIFY_TOKEN:
        print("Validation du Webhook réussie !")
        return request.args.get('hub.challenge')
    else:
        return 'Échec de la validation du Webhook', 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  
                    sender_id = messaging_event["sender"]["id"]        
                    message_text = messaging_event["message"]["text"]  
                    send_message(sender_id, "Bonjour ! Tu as envoyé : " + message_text)
    return "ok", 200

def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v13.0/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

if __name__ == '__main__':
    app.run(debug=True)