import streamlit as st
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from flask import Flask, request, abort

# Initialize Streamlit and Flask
st.title("Line Bot with Streamlit")

# Set your Channel Access Token and Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'b4RQuAF/y/A1MXzS22fBepqVVLigoGuGYqYO+6gYe96v69oiPeBRS03g45m1MKkxJJiNqu9ISXRdGOCmCr/HkYWwnXyoU/ahADFSsz231j6hwojl2xqKXmzaxwIg3Zwrs/ZzdWBLZ1ctJZmkdJMkgAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '8e33786acc72dc61223106d5b9878422'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Flask app to handle the webhook
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    st.write("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# Event handler for receiving messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    # Run Flask app
    from threading import Thread
    def run_flask():
        app.run(port=5000)
    Thread(target=run_flask).start()

    # Streamlit UI
    st.write("This Streamlit app is running alongside a Flask server to handle Line bot webhooks.")
    st.write("Make sure to set your Line webhook URL to `https://<your-domain>/callback`.")
    st.text_area("Webhook request log:")
