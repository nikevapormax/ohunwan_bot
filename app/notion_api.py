import datetime

from notion_client import Client


class NotionAPI:
    def __init__(self, auth):
        self.client = Client(auth=auth)

    def get_database_id(self):
        database = self.client.search(filter={"property": "object", "value": "database"}, page_size=100)
        return database["results"][0]["id"]

    def create_database_page(self, database_id: str, name_list: list, count_list: list):
        for name, count in zip(name_list, count_list):
            properties_new = {
                "횟수/시간": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "code": False,
                                "color": "default",
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                            },
                            "href": None,
                            "plain_text": count,
                            "text": {
                                "content": count,
                                "link": None,
                            },
                            "type": "text"}
                    ],
                    "type": "rich_text",
                },
                "운동이름": {
                    "id": "title",
                    "title": [
                        {
                            "annotations": {
                                "bold": False,
                                "code": False,
                                "color": "default",
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                            },
                            "href": None,
                            "plain_text": name,
                            "text": {"content": name, "link": None},
                            "type": "text",
                        },
                    ],
                    "type": "title",
                },
                "날짜": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "code": False,
                                "color": "default",
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                            },
                            "href": None,
                            "plain_text": datetime.datetime.now().strftime("%Y / %m / %d"),
                            "text": {
                                "content": datetime.datetime.now().strftime("%Y / %m / %d"),
                                "link": None,
                            },
                            "type": "text"}
                    ],
                    "type": "rich_text",
                },
            }
            self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties_new,
            )
