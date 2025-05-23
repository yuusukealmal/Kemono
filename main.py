import os
import re
import sys
import json
import requests
from kemono import Creator, Post

BASE = "https://kemono.su/api/v1"

def requests_creator():
    r = requests.get(f"{BASE}/creators.txt")
    return json.loads(r.content.decode("utf-8"))

def main(arg):
    is_int = re.match(r"^\d+$", arg)
    creators = requests_creator()
    key = "id" if is_int else "name"
    target = next((i for i in creators if str(i[key]) == arg), None)
    if not target:
        print("Creator not found")
        return
    os.makedirs(name, exist_ok=True)
    posts = Creator(**target).get_posts()
    for p in posts:
        post = Post(**p)
        path = os.path.join(name, str(post.id))
        os.makedirs(path, exist_ok=True)
        post.download(path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        main(arg)
    else:
        print("Usage: python main.py <Username or ID>")