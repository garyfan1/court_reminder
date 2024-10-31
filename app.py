from chalice import Chalice, Response, Rate
from bs4 import BeautifulSoup, element, CData
import requests
import lxml
from dotenv import load_dotenv

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

load_dotenv()

app = Chalice(app_name='badminton_checker')

line_bot_api = LineBotApi(os.getenv("LINE_BOT_API_KEY"))
handler = WebhookHandler(os.getenv("WEBHOOK_HANDLER"))

my_line_id = os.getenv("LINE_USER_ID")

# @app.route("/callback", methods=['POST'])
# def callback():
#     request = app.current_request
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#
#     # get request body as text
#     body = request.raw_body.decode()
#
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         print("Invalid signature. Please check your channel access token/channel secret.")
#         return Response(status_code=400)
#
#     return {"msg": 'OK'}
#
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


# @app.route("/")
@app.schedule(Rate(1, unit=Rate.HOURS))
def index(event):
    try:
        start_page_url = """https://webreg.burnaby.ca/webreg/Activities/ActivitiesDetails.asp?aid=8591"""
        resp = requests.get(start_page_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        activity = soup.find(id="activity-course-row")
        date = activity.find(headers="Dates").contents[2].string.strip()
        time = activity.find(headers="Times").contents
        time = time[0].string.strip() + " " + time[2].string.strip()
        day = activity.find(headers="Day").string.strip()
        spots = activity.find(headers="Available").string.strip()

        if int(spots) > 0:
            text = f"{day} {date} {time}\nat Cameron\nnow has {spots} spots"
            print(text)
            line_bot_api.push_message(my_line_id, TextSendMessage(text=text))
        else:
            print("there's no spots left QAQ")
    except:
        text = "somethings wrong"
        line_bot_api.push_message(my_line_id, TextSendMessage(text=text))

    return {"msg": 'OK'}




# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
