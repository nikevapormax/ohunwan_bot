from pprint import pprint

import dotenv
import os

from slack_sdk import WebClient

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


class SlackAPI:
    def __init__(self, token):
        self.client = WebClient(token)  # 슬랙 클라이언트 인스턴스 생성

    def get_channel_id(self, channel_name):
        """
        슬랙 채널ID 조회
        """
        result = self.client.conversations_list()  # 딕셔너리 형태로 들어와서 .data 를 쓸 필요는 없음
        channels = result["channels"]
        channel = list(filter(lambda c: c["name"] == channel_name, channels))[0]
        channel_id = channel["id"]

        return channel_id

    def get_message_ts(self, channel_id, query):
        """
        슬랙 채널 내 메세지 조회
        """
        result = self.client.conversations_history(channel=channel_id)
        messages = result["messages"]
        message = list(filter(lambda x: x["text"] == query, messages))[0]
        message_ts = message["ts"]

        return message_ts

    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        result = self.client.chat_postMessage(
            icon_emoji=":white_check_mark:",
            channel=channel_id,
            thread_ts=message_ts,
            blocks=blocks,
            text=text,
        )

        return result

    def update_thread_message(self, channel_id, message_ts, exercise_name):
        new_block = {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": exercise_name,
                    "emoji": True,
                },
            }
        blocks.insert(-1, new_block)

        result = self.client.chat_update(
            channel=channel_id,
            ts=self.get_thread_reply_ts(channel_id=channel_id, message_ts=message_ts),
            blocks=blocks,
            as_user=True,
        )

        return result

    def get_thread_reply_ts(self, channel_id, message_ts):
        result = self.client.conversations_replies(
            channel=channel_id,
            ts=message_ts,
        )

        return result.data["messages"][1]["ts"]

    def get_thread_reply_information(self, channel_id, message_ts):
        result = self.client.conversations_replies(
            channel=channel_id,
            ts=message_ts,
        )
        pprint(result.data["messages"][1]["blocks"][3:-1])
        return result.data["messages"][1]["blocks"][3:-1]


token = os.environ["SLACK_TOKEN"]
channel_id = os.environ["SLACK_CHANNEL_ID"]
slack = SlackAPI(token)

channel_name = "일반"
query = "오운완"
blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "오운완",
            "emoji": True
        }
    },
    {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": ":tada: 운동횟수 또는 시간을 입력해주세요. :tada:",
            "emoji": True
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "버튼을 눌러 운동을 추가해주세요! :arrow_right:"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "운동 추가",
                "emoji": True
            },
            "value": "click_me_123",
            "url": "https://127.0.0.1:8000/slack/update",
            "action_id": "button-action"
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " "
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "등록",
                "emoji": True
            },
            "value": "click_me_123",
            "url": "https://google.com",
            "action_id": "button-action"
        }
    }
]


# 채널ID 파싱
channel_id = slack.get_channel_id(channel_name)
# # 메세지ts 파싱
message_ts = slack.get_message_ts(channel_id, query)
# # 댓글 달기
# slack.post_thread_message(channel_id, message_ts, text="오운완!!")
# # 댓글 가져오기
# slack.update_thread_message(channel_id, message_ts)
slack.get_thread_reply_information(channel_id, message_ts)
