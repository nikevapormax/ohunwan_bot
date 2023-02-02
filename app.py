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
    say(f"안녕하세요, <@{event['user']}> 님! `오운완`을 입력해주세요!")


@app.message("오운완")
def post_message_register_exercise(client, message):
    channel_id = message["channel"]
    client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text="오운완",
    )


@app.action("button-action")
def handle_register_button_action(ack, client, body):
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
def post_message_content(ack, body):
    ack()

    name_list = []
    count_list = []

    for body_info in body["state"]["values"].items():
        name_list.append(body_info[1]["plain_text_input-action"]["value"].split(" ")[0])
        count_list.append(body_info[1]["plain_text_input-action"]["value"].split(" ")[1])

    db_id = notion_client.create_database()
    notion_client.create_database_page(database_id=db_id, name_list=name_list, count_list=count_list)


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
