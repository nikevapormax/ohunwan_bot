import dotenv
import os

from notion_api import NotionAPI
from slack_api import SlackAPI, blocks
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_client = SlackAPI(token=os.environ["SLACK_BOT_TOKEN"])
notion_client = NotionAPI(auth=os.environ["NOTION_SECRET_KEY"])


@app.event("app_mention")
def say_hello_to_use(event, say):
    say(f"안녕하세요, <@{event['user']}> 님!")
    say(
        blocks=blocks,
        text="오운완",
    )


@app.action("button-action")
def add_register_button_action(ack, client, body):
    ack()

    new_block = {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input-action",
        },
        "label": {
            "type": "plain_text",
            "text": " ",
            "emoji": True,
        }
    }
    blocks.insert(-1, new_block)

    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        blocks=blocks,
        as_user=True,
    )


@app.action("button-action-2")
def post_message_content_to_notion(ack, body, say):
    ack()

    name_list = []
    count_list = []
    error_cnt = 0

    if body["state"]["values"]:
        for body_info in body["state"]["values"].items():
            value = body_info[1]["plain_text_input-action"]["value"]

            if value is not None:
                name_list.append(value.split(" ")[0])
                count_list.append(value.split(" ")[1])
            else:
                error_cnt += 1

        if error_cnt >= 1:
            say("`운동이름 횟수(시간)`을 입력해주세요!")
        else:
            db_id = notion_client.get_database_id()
            notion_client.create_database_page(database_id=db_id, name_list=name_list, count_list=count_list)

            say("`노션`에 입력하신 운동정보가 등록되었습니다! `노션에서 확인`해주세요!")
    else:
        say("`운동이름 횟수(시간)`을 입력해주세요!")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
