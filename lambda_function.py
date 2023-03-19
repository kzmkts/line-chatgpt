import os
import logging
import openai
import signal
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

logger = logging.getLogger()
logger.setLevel(logging.INFO)

line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])
openai.api_key = os.environ["OPENAI_API_KEY"]

API_TIMEOUT = 15


class TimeoutException(Exception):
    pass


def get_signature(event):
    headers = {k.lower(): v for k, v in event["headers"].items()}
    return headers.get("x-line-signature", None)


def lambda_handler(event, context):
    signature = get_signature(event)
    body = event["body"]

    if not signature:
        logger.error("X-Line-Signature header is missing")
        return {
            "statusCode": 400,
            "body": "Bad Request"
        }

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.error("Invalid signature")
        return {
            "statusCode": 400,
            "body": "Invalid signature"
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": "Internal Server Error"
        }

    return {
        "statusCode": 200,
        "body": "OK"
    }


def call_openai_api(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ]
    )
    return response.choices[0].message["content"].strip()


def timeout_handler(signum, frame):
    raise TimeoutException()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(API_TIMEOUT - 1)

    try:
        reply_text = call_openai_api(user_input)
    except TimeoutException:
        reply_text = "Sorry, the assistant took too long to respond. Please try again."
    finally:
        signal.alarm(0)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
