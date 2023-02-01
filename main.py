import dotenv
import os

from fastapi import FastAPI
from notion_client import Client
from slack_api import SlackAPI

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

app = FastAPI()
slack_client = SlackAPI(token=os.environ["SLACK_TOKEN"])
notion_client = Client(auth=os.environ["NOTION_SECRET_KEY"])
pages = notion_client.search(filter={"property": "object", "value": "page"}, page_size=10)


@app.get("/slack")
async def get_channel_id(channel_name: str):
    # 채널 id 조회
    channel_id = slack_client.get_channel_id(channel_name=channel_name)
    # 슬랙 채널 내 메세지 ts 조회
    message_ts = slack_client.get_message_ts(channel_id=channel_id, query="오운완")

    # 조회된 채널 id와 메세지 ts에 댓글 달기
    slack_client.post_thread_message(channel_id=channel_id, message_ts=message_ts, text="오운완!!")

    return {"channel_id": channel_id, "message_ts": message_ts}


@app.put("/slack/update")
async def update_message_reply(channel_id: str, message_ts: str, exercise_name: str):
    # thread 내 bot user의 메세지 수정
    slack_client.update_thread_message(channel_id=channel_id, message_ts=message_ts, exercise_name=exercise_name)
    return {"status": "done"}


@app.post("/slack/send")
async def send_message_info_to_notion(channel_id: str, message_ts: str):
    page_title_find = []
    count = []

    info_list = slack_client.get_thread_reply_information(channel_id=channel_id, message_ts=message_ts)
    for info in info_list:
        page_title_find.append(info["label"]["text"])

    return {"page_title_find": page_title_find}
