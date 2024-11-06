import json
import requests
import dotenv
import os
from urllib.parse import urlparse


dotenv.load_dotenv()

TENDER_API_KEY = os.getenv("TENDER_API_KEY")


def authorized_request(url):
    headers = {
        "X-Tender-Auth": TENDER_API_KEY,
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_paged_objects(url, key):
    all_objects = []
    page = 1
    while True:
        paged_url = f"{url}?page={page}"
        response = authorized_request(paged_url)
        objects = response.get(key, [])
        if not objects:
            break
        all_objects.extend(objects)
        if len(objects) < response.get("per_page", 30):
            break
        page += 1
    return all_objects


def get_categories():
    url = "https://api.tenderapp.com/nodebox/categories"
    return authorized_request(url)["categories"]


def get_discussions(category_id):
    url = f"https://api.tenderapp.com/nodebox/categories/{category_id}/discussions"
    return get_paged_objects(url, "discussions")


def get_discussion(discussion_id):
    url = f"https://api.tenderapp.com/nodebox/discussions/{discussion_id}"
    return authorized_request(url)


def get_comments(discussion_id):
    url = f"https://api.tenderapp.com/nodebox/discussions/{discussion_id}/comments"
    return get_paged_objects(url, "comments")


categories = get_categories()
for category in categories:
    slug = category["permalink"]
    category_id = urlparse(category["href"]).path.split("/")[-1]
    print(slug, flush=True)
    category_dir = f"data/categories/{slug}"
    os.makedirs(category_dir, exist_ok=True)
    category_file = os.path.join(category_dir, "category.json")
    with open(category_file, "w") as f:
        f.write(json.dumps(category, indent=2))

    for discussion in get_discussions(category_id):
        discussion_id = urlparse(discussion["href"]).path.split("/")[-1]
        print(f'  {discussion_id} {discussion["title"]}', flush=True)
        full_discussion = get_discussion(discussion_id)
        discussion_dir = os.path.join(category_dir, discussion_id)
        os.makedirs(discussion_dir, exist_ok=True)
        discussion_file = os.path.join(discussion_dir, "discussion.json")
        with open(discussion_file, "w") as f:
            f.write(json.dumps(full_discussion, indent=2))

        comments = get_comments(discussion_id)
        for comment in comments:
            comment_id = comment["number"]
            comment_dir = os.path.join(discussion_dir, "comments", str(comment_id))
            os.makedirs(comment_dir, exist_ok=True)
            comment_file = os.path.join(comment_dir, f"comment.json")
            with open(comment_file, "w") as f:
                f.write(json.dumps(comment, indent=2))

            for asset in comment.get("assets", []):
                asset_url = asset["download_path"]
                filename = asset["filename"]
                print(filename, flush=True)
                asset_file = os.path.join(comment_dir, filename)
                if not os.path.exists(asset_file):
                    print(f"    {filename}", flush=True)
                    response = requests.get(asset_url)
                    try:
                        response.raise_for_status()
                        with open(asset_file, "wb") as f:
                            f.write(response.content)
                    except requests.exceptions.RequestException as e:
                        print(
                            f"    Warning: Failed to download {filename}. Error: {e}",
                            flush=True,
                        )
