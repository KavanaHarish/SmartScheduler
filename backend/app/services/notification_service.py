import os
from twilio.rest import Client

TW_SID = os.getenv('TWILIO_ACCOUNT_SID')
TW_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TW_PHONE = os.getenv('TWILIO_PHONE')

client = None
if TW_SID and TW_TOKEN:
    try:
        client = Client(TW_SID, TW_TOKEN)
    except Exception as e:
        print('Twilio init error', e)

def send_sms(to, body):
    if not client:
        print('[SMS MOCK] To:', to, 'Msg:', body)
        return {'mock': True}
    try:
        msg = client.messages.create(body=body, from_=TW_PHONE, to=to)
        return {'sid': msg.sid}
    except Exception as e:
        print('Twilio send error', e)
        return {'error': str(e)}

def send_bulk_sms(numbers, body):
    results = []
    for n in numbers:
        results.append(send_sms(n, body))
    return results
