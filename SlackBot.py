import flask
import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import send_from_directory
from slackeventsapi import SlackEventAdapter
import urllib.request, json



env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


zipCode = "281184"
f = open("citites.txt", "r")
amap = ["one",""]
map = f.read().replace("\n",',').split(",")

app = flask.Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


client.chat_postMessage(channel='#test', text="Hello World!")

BOT_ID = client.api_call("auth.test")['user_id']


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    return "Hello World0.03"

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()