import os
import asyncio
from notion_client import AsyncClient
from dotenv import load_dotenv

load_dotenv()

NOTION_API_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

notion = AsyncClient(auth=NOTION_API_TOKEN)

__all__ = ["fetch_all_notion_pages"]


def flatten_rich_text(rich_text_array):
    return ''.join([rt.get("plain_text", "") for rt in rich_text_array])


def extract_title(properties):
    for key, prop in properties.items():
        if prop.get("type") == "title":
            title_obj = prop.get("title", [])
            if title_obj:
                return flatten_rich_text(title_obj)
    return "Untitled Page"


def extract_text_from_row(properties):
    lines = []
    for key, prop in properties.items():
        prop_type = prop.get("type")
        if prop_type == "title":
            lines.append(f"# {flatten_rich_text(prop['title'])}")
        elif prop_type == "rich_text":
            lines.append(flatten_rich_text(prop["rich_text"]))
        elif prop_type == "number":
            lines.append(f"{key}: {prop['number']}")
        elif prop_type == "select" and prop["select"]:
            lines.append(f"{key}: {prop['select']['name']}")
        elif prop_type == "multi_select":
            tags = [tag['name'] for tag in prop['multi_select']]
            lines.append(f"{key}: {', '.join(tags)}")
        elif prop_type == "checkbox":
            lines.append(f"{key}: {'Yes' if prop['checkbox'] else 'No'}")
    return '\n'.join(lines)


async def fetch_all_rows(database_id):
    results = []
    cursor = None
    while True:
        response = await notion.databases.query(
            database_id=database_id,
            start_cursor=cursor
        ) if cursor else await notion.databases.query(database_id=database_id)

        results.extend(response["results"])
        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")
    return results


async def extract_block_text(block_id, indent=0):
    content = []
    children = await notion.blocks.children.list(block_id=block_id)

    for block in children["results"]:
        block_type = block["type"]

        if block_type in [
            "paragraph", "heading_1", "heading_2", "heading_3",
            "bulleted_list_item", "numbered_list_item"
        ]:
            rich_text = block[block_type].get("rich_text", [])
            text = flatten_rich_text(rich_text)
            prefix = " " * indent

            if block_type.startswith("heading"):
                level = int(block_type.split("_")[1])
                content.append(f"{prefix}{'#' * level} {text}")
            elif block_type == "bulleted_list_item":
                content.append(f"{prefix}- {text}")
            elif block_type == "numbered_list_item":
                content.append(f"{prefix}1. {text}")
            else:
                content.append(f"{prefix}{text}")

        elif block_type == "child_page":
            content.append(f"\n{' ' * indent}## Child Page: {block['child_page']['title']}")

        elif block_type == "column_list":
            content.append(f"\n{' ' * indent}-- Start Column Layout --")
            column_children = await notion.blocks.children.list(block_id=block["id"])
            for column in column_children["results"]:
                if column["type"] == "column":
                    content.append(f"\n{' ' * (indent + 2)}-- Column --")
                    column_content = await extract_block_text(column["id"], indent + 4)
                    content.append(column_content)
            content.append(f"\n{' ' * indent}-- End Column Layout --")

        elif block_type == "column":
            continue 

        else:
            pass  

    return '\n'.join(content)


async def fetch_all_notion_pages():
    rows = await fetch_all_rows(DATABASE_ID)
    all_pages = []

    for row in rows:
        title = extract_title(row["properties"])
        page_id = row["id"]
        props_content = extract_text_from_row(row["properties"])
        block_content = await extract_block_text(page_id)
        combined_text = f"{props_content}\n\n{block_content}"

        all_pages.append({
            "title": title,
            "text": combined_text
        })

    return all_pages



if __name__ == "__main__":
    async def main():
        print("Fetching pages from Notion...")
        pages = await fetch_all_notion_pages()
        print(f"\nFound {len(pages)} pages")
        for idx, page in enumerate(pages, 1):
            print(f"\n--- Page {idx}: {page['title']} ---")
            print(page["text"])

    asyncio.run(main())
