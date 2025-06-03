import os
import time
import requests
from mimetypes import guess_type

BASE = "https://kemono.su/api/v1"
IMG_BASE = "https://img.kemono.su/thumbnail/data"
ATTACHMENT_BASE = "https://c1.kemono.su/data"

def is_image(file: dict) -> bool:
    mimetype, _ = guess_type(file["path"])
    return mimetype is not None and mimetype.startswith("image")

class Creator:
    def __init__(self, id, name, service, indexed, updated, favorited):
        self.id = id
        self.name = name
        self.service = service
        self.indexed = indexed
        self.updated = updated
        self.favorited = favorited

    def get_user(self):
        return requests.get(f"{BASE}/{self.service}/user/{self.id}/profile").json()

    def get_posts(self):
        return requests.get(f"{BASE}/{self.service}/user/{self.id}/posts").json()

class Post:
    def __init__(self, id, user, service, title, content, embed, shared_file, added, published, edited, file, attachments, poll, captions, tags):
        self.id = id
        self.user = user
        self.service = service
        self.title = title
        self.content = content
        self.embed = embed
        self.shared_file = shared_file
        self.added = added
        self.published = published
        self.edited = edited
        self.file = file
        self.attachments = attachments
        self.poll = poll
        self.captions = captions
        self.tags = tags
        self.files = [self.file] + list(self.attachments)

    def get_post(self):
        return requests.get(f"{BASE}/{self.service}/user/{self.user}/post/{self.id}").json()

    def get_post_revision(self):
        return requests.get(f"{BASE}/{self.service}/user/{self.user}/post/{self.id}/revisions").json()

    def download(self, path):
        for file in self.files:
            print(f"Downloading {file['name']}")
            base = IMG_BASE if is_image(file) else ATTACHMENT_BASE
            url = f"{base}{file['path']}"
            filepath = os.path.join(path, file["name"])
            if is_image(file):
                with open(os.path.join(path, file["name"]), "wb") as f:
                    f.write(requests.get(url).content)
            else:
                with requests.get(url, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    with open(filepath, "wb") as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)