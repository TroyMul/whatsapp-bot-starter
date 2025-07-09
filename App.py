import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

FAQ_ANSWERS = {
    "hours": "Our working hours are 9am to 5pm, Monday to Friday.",
    "pricing": "Our prices start from $10 per service.",
    "location": "We are located at 123 Main Street, Your City.",
}

def get_faq_answer(message):
    for key, ans in FAQ_ANSWERS.items():
        if key in message.lower():
            return ans
    return None

def generate_chatgpt_reply(message):
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=150,
        temperature=0.7,
    )
    return resp.choices[0].text.strip()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    faq = get_faq_answer(msg)
    if faq:
        resp.message(faq)
    else:
        ai = generate_chatgpt_reply(msg)
        resp.message(ai)
    return str(resp)

if __name__ == "__main__":
    app.run()
