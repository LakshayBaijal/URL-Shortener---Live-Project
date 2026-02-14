import json
import os
from filelock import FileLock

URLS_FILE = "data/urls.json"
META_FILE = "data/meta.json"
LOCK_FILE = "data/lock.lock"


def read_urls():
    if not os.path.exists(URLS_FILE):
        return {}
    
    with FileLock(LOCK_FILE):
        with open(URLS_FILE, "r") as file:
            return json.load(file)


def write_urls(data):
    with FileLock(LOCK_FILE):
        with open(URLS_FILE, "w") as file:
            json.dump(data, file, indent=4)


def read_meta():
    if not os.path.exists(META_FILE):
        return {"counter": 1}
    
    with FileLock(LOCK_FILE):
        with open(META_FILE, "r") as file:
            return json.load(file)


def write_meta(data):
    with FileLock(LOCK_FILE):
        with open(META_FILE, "w") as file:
            json.dump(data, file, indent=4)
