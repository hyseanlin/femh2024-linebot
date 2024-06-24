import streamlit as st
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import abort

# Replace these with your actual Line Bot API credentials
LINE_CHANNEL_ACCESS_TOKEN = 'b4RQuAF/y/A1MXzS22fBepqVVLigoGuGYqYO+6gYe96v69oiPeBRS03g45m1MKkxJJiNqu9ISXRdGOCmCr/HkYWwnXyoU/ahADFSsz231j6hwojl2xqKXmzaxwIg3Zwrs/ZzdWBLZ1ctJZmkdJMkgAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '8e33786acc72dc61223106d5b9878422'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Function to handle messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# Streamlit app
st.title("LINE Bot Echo App")
st.write("This is a simple LINE bot that echoes what the user types.")

# To display the access token and secret for convenience (optional)
st.write("Your LINE Channel Access Token:", LINE_CHANNEL_ACCESS_TOKEN)
st.write("Your LINE Channel Secret:", LINE_CHANNEL_SECRET)

st.write("To use this bot, set the webhook URL in the LINE Developers Console to point to this app's URL.")

# Use the sidebar for the webhook interface (simulated for local testing)
if st.sidebar.checkbox('Simulate LINE Message'):
    user_id = st.sidebar.text_input('User ID', 'U1234567890')
    user_message = st.sidebar.text_input('User Message', 'Hello, LINE bot!')

    if st.sidebar.button('Send Message'):
        event = MessageEvent(type='message', reply_token='dummy', source={'userId': user_id}, message={'type': 'text', 'id': '1', 'text': user_message})
        handle_message(event)
        st.sidebar.write(f'Sent message: {user_message}')

st.write("Ensure your server is publicly accessible and properly configured to handle LINE webhook events.")

# Define a function to listen to the webhook events (for deployment)
def webhook(request):
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Note: Deployment instructions will vary depending on where you're hosting the app.
# For example, if using Heroku, you'll need to add a Procfile and configure your app to listen to HTTP requests.