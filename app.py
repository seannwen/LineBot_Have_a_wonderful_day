from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
# from var.variable import ACCESS_TOKEN, CHANNEL_SECRET
import os
import nba

from datetime import datetime

app = Flask(__name__)

# Channel Access Token
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
#access_token = 'ACCESS_TOKEN'
line_bot_api = LineBotApi(ACCESS_TOKEN)

# Channel Secret
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')
#channel_secret = 'CHANNEL_SECRET'
#handler = WebhookHandler(channel_secret)
handler = WebhookHandler(CHANNEL_SECRET)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)

    date = []
    datetime = datetime.today()
    date = datetime.strftime("%Y%m%d")


    if message.text == 'NBA':
        #message = nba
        web = nba.get_web_data(date)  # get the data from website
        message = nba.get_daily_score(web)
        line_bot_api.reply_message(event.reply_token, message)
    else:

    #nba_response = 'fuck' #blablablabla
        #message = TextSendMessage(text=event.message.text)
        #line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
