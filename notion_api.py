import datetime

from notion_client import Client


class NotionAPI:
    def __init__(self, auth):
        self.client = Client(auth=auth)

    def create_database(self):
        pages = self.client.search(filter={"property": "object", "value": "page"}, page_size=100)

        page_id = pages["results"][0]["id"]
        parent_id = {"type": "page_id", "page_id": page_id}
        today = datetime.datetime.now().strftime("%Y / %m / %d")
        title_value = [{"type": "text", "text": {"content": today, "link": None}}]
        icon_value = {"emoji": "🏋", "type": "emoji"}

        property_values = {}
        title_1 = {
            "운동이름": {
                "id": "title",
                "name": "운동이름",
                "title": {},
                "type": "title",
            }
        }
        title_2 = {
            "횟수/시간": {
                "name": "횟수/시간",
                "rich_text": {},
                "type": "rich_text",
            }
        }
        property_values.update(title_1)
        property_values.update(title_2)

        db = self.client.databases.create(
            parent=parent_id,
            title=title_value,
            icon=icon_value,
            properties=property_values
        )

        return db["id"]

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
            }
            self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties_new,
            )
