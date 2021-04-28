from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from var.variable import ACCESS_TOKEN, CHANNEL_SECRET
import os
import nba
import ptt

from datetime import datetime, timedelta

app = Flask(__name__)

# Channel Access Token

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

line_bot_api = LineBotApi(ACCESS_TOKEN)

# Channel Secret
CHANNEL_SECRET = os.environ.get(CHANNEL_SECRET)
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
    split_message = message.text.split(' ')
    error_message = "請參照格式 'PTT 版名'\nEx: PTT nba"
    page_not_found_message = "此版不存在，請重新輸入。"
    date = []
    today = datetime.today()
    date = today.strftime("%Y%m%d")

    # NBA & PTT
    if split_message[0].lower() == 'nba':
        nba_team_dict = nba.team_name()
        nba_web = nba.get_web_data(date)  # get the daily data from website
        nba_daily_score = nba.get_daily_score(nba_web)

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=nba_daily_score))

    elif split_message[0].lower() == 'ptt':
            current_page = 'https://www.ptt.cc/bbs/{}/index.html'.format(split_message[1])
            articles_info = []
            bs4_html = ptt.get_bs4_html(current_page)
            if not bs4_html.find('title') or bs4_html.find('title').text == '404':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=page_not_found_message))
            else:
                articles_info = ptt.browse(articles_info, bs4_html)
                articles = '\n'.join(articles_info)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=articles))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))



    # if len(split_message) == 2:
    #     if split_message[0].lower() == 'ptt':
    #         current_page = 'https://www.ptt.cc/bbs/{}/index.html'.format(split_message[1])
    #         articles_info = []
    #         bs4_html = ptt.get_bs4_html(current_page)
    #         if not bs4_html.find('title') or bs4_html.find('title').text == '404':
    #             line_bot_api.reply_message(event.reply_token, TextSendMessage(text=page_not_found_message))
    #         else:
    #             articles_info = ptt.browse(articles_info, bs4_html)
    #             articles = '\n'.join(articles_info)
    #             line_bot_api.reply_message(event.reply_token, TextSendMessage(text=articles))
    #     else:
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))
    # else:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=error_message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
