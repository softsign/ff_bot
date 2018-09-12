import os
from yahooff import League
from yql3 import *
from yql3.storage import FileTokenStore

if __name__ == '__main__':


    try:
        bot_id = os.environ["BOT_ID"]
    except KeyError:
        bot_id = 1

    try:
        webhook_url = os.environ["WEBHOOK_URL"]
    except KeyError:
        webhook_url = 1

    league_id = os.environ["LEAGUE_ID"]

    try:
        year = os.environ["LEAGUE_YEAR"]
    except KeyError:
        year=2018

    #league = League(league_id, year)


    # yahoo oauth api (consumer) key and secret
    with open("./authentication/private.txt", "r") as auth_file:
        auth_data = auth_file.read().split("\n")
    consumer_key = auth_data[0]
    consumer_secret = auth_data[1]

    # yahoo oauth process
    y3 = ThreeLegged(consumer_key, consumer_secret)
    _cache_dir = "./authentication/oauth_token"
    if not os.access(_cache_dir, os.R_OK):
        os.mkdir(_cache_dir)

    token_store = FileTokenStore(_cache_dir, secret="sasfasdfdasfdaf")
    stored_token = token_store.get("foo")


    if not stored_token:
        request_token, auth_url = y3.get_token_and_auth_url()

        print("Visit url %s and get a verifier string" % auth_url.decode('UTF-8'))
        verifier = input("Enter the code: ")
        token = y3.get_access_token(request_token, verifier)
        token_store.set("foo", token)

    print("\nSuccess, I think.")
