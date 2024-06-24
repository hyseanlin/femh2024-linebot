import streamlit as st
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Request

# Define your LINE Bot credentials
CHANNEL_ACCESS_TOKEN = 'b4RQuAF/y/A1MXzS22fBepqVVLigoGuGYqYO+6gYe96v69oiPeBRS03g45m1MKkxJJiNqu9ISXRdGOCmCr/HkYWwnXyoU/ahADFSsz231j6hwojl2xqKXmzaxwIg3Zwrs/ZzdWBLZ1ctJZmkdJMkgAdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '8e33786acc72dc61223106d5b9878422'

# Initialize the LINE Bot API and Webhook Handler
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

st.title("LINE Bot Echo App")

# Endpoint for handling webhook requests
def handle_webhook(request: Request):
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        st.error("Invalid signature. Please check your channel access token/channel secret.")
        return 'Error', 400

    return 'OK', 200

# Define a callback for handling messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_token = event.reply_token
    user_message = event.message.text
    line_bot_api.reply_message(reply_token, TextSendMessage(text=user_message))
    st.write(f"Echoed message: {user_message}")

# Streamlit interface for webhook handling
st.write("Webhook URL: Set this URL in the LINE Developers Console")
st.write("Webhook handling is in progress...")

# Handle webhook request
request = st.experimental_get_query_params()
if request:
    handle_webhook(request)
