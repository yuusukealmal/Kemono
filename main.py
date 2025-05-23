import os
import json
import requests
from kemono import Creator, Post

BASE = "https://kemono.su/api/v1"

def requests_creator():
    r = requests.get(f"{BASE}/creators.txt")
    return json.loads(r.content.decode("utf-8"))

def main():
    creators = requests_creator()
    name = input("Please Enter Creator: ")
    target = next((i for i in creators if i["name"] == name), None)
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
    main()