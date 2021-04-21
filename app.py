from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from var.variable import ACCESS_TOKEN, CHANNEL_SECRET
import os
import nba

app = Flask(__name__)

# Channel Access Token
#access_token = os.environ.get('ACCESS_TOKEN')
access_token = 'ACCESS_TOKEN'
line_bot_api = LineBotApi(access_token)

# Channel Secretos.environ.get('ACCESS_TOKEN')
#channel_secret = os.environ.get('CHANNEL_SECRET')
channel_secret = 'CHANNEL_SECRET'
handler = WebhookHandler(channel_secret)

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
    error_message = "請輸入想查詢的NBA隊名縮寫(Ex: LAL)"
    team_not_found_message = "查無此隊伍，請重新輸入。"
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
