import streamlit as st
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort

LINE_CHANNEL_ACCESS_TOKEN = 'b4RQuAF/y/A1MXzS22fBepqVVLigoGuGYqYO+6gYe96v69oiPeBRS03g45m1MKkxJJiNqu9ISXRdGOCmCr/HkYWwnXyoU/ahADFSsz231j6hwojl2xqKXmzaxwIg3Zwrs/ZzdWBLZ1ctJZmkdJMkgAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '8e33786acc72dc61223106d5b9878422'

# Initialize a Flask app
app = Flask(__name__)

# Set up LINE bot credentials
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Streamlit section
st.title("LINE Bot Echo App")
st.write("This app echoes back whatever you type in your LINE chat.")

# Webhook endpoint
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    st.write("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except Exception as e:
        st.write("Exception: " + str(e))
        abort(400)

    return 'OK'

# Event handler for receiving messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    st.write("Received message: " + text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
    )

# Run Flask app
if __name__ == "__main__":
    app.run(port=5000)
d to add a Procfile and configure your app to listen to HTTP requests.