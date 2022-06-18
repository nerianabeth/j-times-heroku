import flask
import os
import slack
from pathlib import Path
from dotenv import load_dotenv
from flask import send_from_directory, Response, request
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


# client.chat_postMessage(channel='#test', text="Hello World!")

BOT_ID = client.api_call("auth.test")['user_id']

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

        # return
    if BOT_ID != user_id:
        for city in map:
            if text.lower() in city.lower():
                zipCode = city.split("|")[-1]
                print(city)
                with urllib.request.urlopen(
                        "https://www.hebcal.com/shabbat?cfg=json&geonameid=" + zipCode + "&M=on&lg=h") as url:
                    data = json.loads(url.read().decode())
                    data = "הדלקת נרות, שבת " + data.get("items")[0].get("memo")+" ב- " +data.get("location").get("title")+" תכנס ב- " + data.get("items")[0].get("title").split(": ")[-1]
                    client.chat_postMessage(channel=channel_id,text=data)


@app.route('/shabbat')
def shabbatZmanim():
    return  Response(>>>), 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.png')

@app.route('/')
@app.route('/home')
def home():
    return "Hello World0.14"

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()