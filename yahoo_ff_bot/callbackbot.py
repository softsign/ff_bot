'''

This implements a bot that can listen at a callback URL and respond to messages in a GroupMe group

To make this work, install gunicorn (pip install gunicorn), then run

gunicorn -w 4 callbackbot:app -b 1.1.1.1:50000

(replace the IP and port with the IP (or domain) and port of your choosing)


'''


import os
import sys
from yahoo_ff_bot import ff_bot
from yahooff import League
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    '''same as main loop setup in ff_bot.py'''
    try:
        bot_id = os.environ["BOT_ID"]
    except KeyError:
        bot_id = 1

    try:
        webhook_url = os.environ["WEBHOOK_URL"]
    except KeyError:
        webhook_url = 1

    try:
        league_id = os.environ["LEAGUE_ID"]
    except KeyError:
        league_id = 1

    try:
        year = os.environ["LEAGUE_YEAR"]
    except KeyError:
        year = 2018

    try:
        yahoo_consumer_key = os.environ["YAHOO_CONSUMER_KEY"]
    except KeyError:
        yahoo_consumer_key = 1

    try:
        yahoo_consumer_secret = os.environ["YAHOO_CONSUMER_SECRET"]
    except KeyError:
        yahoo_consumer_secret = 1

    league = League(league_id, year, yahoo_consumer_key, yahoo_consumer_secret)

    if data['text'] == '!scores':
        text = ff_bot.get_scoreboard(league)
        send_message(text)
    elif data['text'] == '!matchups':
        text = ff_bot.get_matchups(league)
        send_message(text)
    elif data['text'] == '!close':
        text = ff_bot.get_close_scores(league)
        send_message(text)
    elif data['text'] == '!power':
        text = ff_bot.get_power_rankings(league)
        send_message(text)
    elif data['text'] == '!luck':
        text = ff_bot.get_luck(league)
        send_message(text)
    elif data['text'] == '!standings':
        text = ff_bot.get_standings(league)
        send_message(text)
    elif data['text'] == '!trophies':
        text = ff_bot.get_trophies(league)
        send_message(text)
    elif data['text'] == '!help':
        text = "I understand the following commands: !scores, !matchups, !close, !power, !luck, !standings, !trophies"
        send_message(text)

    return "ok", 200

def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id': os.getenv('BOT_ID'),
        'text': msg,
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()


def log(msg):
    print(str(msg))
    sys.stdout.flush()