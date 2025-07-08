from flask import Flask, request, render_template, jsonify
from models import save_event, collection
from bson.json_util import dumps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    author = data['sender']['login']

    if event_type == "push":
        to_branch = data['ref'].split('/')[-1]
        save_event("push", author, to_branch=to_branch)

    elif event_type == "pull_request":
        action = data['action']
        if action in ["opened", "reopened"]:
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            save_event("pull_request", author, from_branch, to_branch)
        elif data.get("pull_request", {}).get("merged"):
            from_branch = data['pull_request']['head']['ref']
            to_branch = data['pull_request']['base']['ref']
            save_event("merge", author, from_branch, to_branch)

    return '', 200

@app.route('/events', methods=['GET'])
def get_events():
    events = collection.find().sort("timestamp", -1)
    return dumps(events)

if __name__ == '__main__':
    app.run(debug=True)
