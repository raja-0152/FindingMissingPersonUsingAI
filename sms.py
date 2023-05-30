from twilio.rest import Client

def send_sms(account_sid, auth_token, from_number, to_number, message):
    
    try:
        client = Client(account_sid, auth_token)
        response = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        print("SMS sent successfully.")
        print("Message SID:", response.sid)
    except Exception as e:
        print("Error sending SMS:", str(e))
    