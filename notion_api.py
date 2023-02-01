import dotenv
import os

from notion_client import Client
from pprint import pprint

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

notion = Client(auth=os.environ["NOTION_SECRET_KEY"])
pages = notion.search(filter={"property": "object", "value": "page"}, page_size=10)


def update_notion(page_title_find: list, count: list):
    for page in pages["results"]:
        page_title = page["properties"]["title"]["title"][0]["plain_text"]

        if page_title in page_title_find:
            revise_properties = page["properties"]

            del revise_properties["kind"]
            del revise_properties["title"]
            del revise_properties["count"]["id"]
            del revise_properties["count"]["type"]

            revise_properties["count"]["number"] = count[page_title_find.index(page_title)]

            notion.pages.update(page_id=page["id"], properties=revise_properties)


update_notion(count=[20, 20, 30])


# cursor_id = pages["next_cursor"]
# has_more = pages["has_more"]
#
# while has_more:
#     pages = notion.search(filter={"property": "object", "value": "page"}, start_cursor=cursor_id)
#
#     has_more = pages["has_more"]
#     if has_more:
#         cursor_id = pages["next_cursor"]