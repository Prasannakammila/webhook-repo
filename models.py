from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["webhookDB"]
collection = db["events"]

def save_event(event_type, author, from_branch=None, to_branch=None):
    timestamp = datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
    if event_type == "push":
        message = f'{author} pushed to {to_branch} on {timestamp}'
    elif event_type == "pull_request":
        message = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}'
    elif event_type == "merge":
        message = f'{author} merged branch {from_branch} to {to_branch} on {timestamp}'
    else:
        return

    collection.insert_one({"message": message, "timestamp": timestamp})
