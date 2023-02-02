import dotenv
import os

from fastapi import FastAPI
from notion_api import NotionAPI
from slack_api import SlackAPI

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

app = FastAPI()
slack_client = SlackAPI(token=os.environ["SLACK_TOKEN"])
notion_client = NotionAPI(auth=os.environ["NOTION_SECRET_KEY"])


@app.get("/slack")
async def get_channel_id(channel_name: str):
    channel_id = slack_client.get_channel_id(channel_name=channel_name)
    message_ts = slack_client.get_message_ts(channel_id=channel_id, query="오운완")

    # 조회된 채널 id와 메세지 ts에 댓글 달기
    slack_client.post_thread_message(channel_id=channel_id, message_ts=message_ts, text="오운완!!")

    return {"channel_id": channel_id, "message_ts": message_ts}


@app.put("/slack/update")
async def update_message_reply(channel_id: str, message_ts: str, exercise_name_count: str):
    # thread 내 bot user의 메세지 수정
    slack_client.update_thread_message(
        channel_id=channel_id,
        message_ts=message_ts,
        exercise_name_count=exercise_name_count,
    )

    return {"status": "done"}


@app.post("/slack/send")
async def send_message_info_to_notion(channel_id: str, message_ts: str):
    name_list = []
    count_list = []

    info_list = slack_client.get_thread_reply_information(channel_id=channel_id, message_ts=message_ts)
    for info in info_list:
        name_list.append(info["text"]["text"].split(" ")[0])
        count_list.append(info["text"]["text"].split(" ")[1])

    # notion에 데이터베이스 및 페이지 생성
    database_id = notion_client.create_database()
    notion_client.create_database_page(
        database_id=database_id,
        name_list=name_list,
        count_list=count_list,
    )

    return {"name_list": name_list, "count_list": count_list}
