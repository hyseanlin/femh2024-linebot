import streamlit as st
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
import os

# Set up the LINE Bot API and WebhookHandler
CHANNEL_ACCESS_TOKEN = 'b4RQuAF/y/A1MXzS22fBepqVVLigoGuGYqYO+6gYe96v69oiPeBRS03g45m1MKkxJJiNqu9ISXRdGOCmCr/HkYWwnXyoU/ahADFSsz231j6hwojl2xqKXmzaxwIg3Zwrs/ZzdWBLZ1ctJZmkdJMkgAdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '8e33786acc72dc61223106d5b9878422'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Create a public URL using Streamlit's built-in functionality
if "WEBHOOK_URL" not in st.session_state:
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    port = os.getenv('PORT', 80)
    st.session_state["WEBHOOK_URL"] = f"http://{ip_address}:{port}/callback"

st.write(f"Public URL: {st.session_state['WEBHOOK_URL']}")

# Streamlit app layout
st.title('LINE Bot Echo Server')
st.write('This server echoes back any message sent to it.')

# Handling incoming webhook requests
@st.experimental_singleton
def get_message_store():
    return []

message_store = get_message_store()

def handle_message(event):
    text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
    )
    message_store.append(f"User: {text}")

# Create a placeholder for the request body
if "request_body" not in st.session_state:
    st.session_state["request_body"] = ""

# Function to simulate receiving a request
def receive_request():
    st.session_state["request_body"] = st.experimental_get_query_params().get("body", [""])[0]
    signature = st.experimental_get_query_params().get("signature", [""])[0]
    body = st.session_state["request_body"]

    if signature and body:
        try:
            body_dict = json.loads(body)
            handler.handle(body, signature)
            for event in body_dict['events']:
                if event['type'] == 'message' and event['message']['type'] == 'text':
                    handle_message(MessageEvent(
                        message=TextMessage(text=event['message']['text']),
                        reply_token=event['replyToken'],
                        source=event['source']
                    ))
            st.success("Message handled successfully!")
        except InvalidSignatureError:
            st.error("Invalid signature. Please check your channel access token and secret.")
        except json.JSONDecodeError:
            st.error("Invalid JSON format in the request body.")
    else:
        st.error("Please provide both the X-Line-Signature and Request Body.")

# Add a button to simulate receiving a request
st.button("Receive Request", on_click=receive_request)

# Display messages
st.write("Messages received:")
for msg in message_store:
    st.write(msg)

