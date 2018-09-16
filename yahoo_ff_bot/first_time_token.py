import os
from yql3 import *
from yql3.storage import FileTokenStore

if __name__ == '__main__':

    try:
        yahoo_consumer_key = os.environ["YAHOO_CONSUMER_KEY"]
    except KeyError:
        yahoo_consumer_key = 1

    try:
        yahoo_consumer_secret = os.environ["YAHOO_CONSUMER_SECRET"]
    except KeyError:
        yahoo_consumer_secret = 1

    # yahoo oauth process
    y3 = ThreeLegged(yahoo_consumer_key, yahoo_consumer_secret)
    _cache_dir = "./.oauth_token_cache"
    if not os.access(_cache_dir, os.R_OK):
        os.mkdir(_cache_dir)

    token_store = FileTokenStore(_cache_dir, secret="sasfasdfdasfdafs")
    stored_token = token_store.get("foo")

    if not stored_token:
        request_token, auth_url = y3.get_token_and_auth_url()

        print("Visit url %s and get a verifier string" % auth_url.decode('UTF-8'))
        verifier = input("Enter the code: ")
        token = y3.get_access_token(request_token, verifier)
        token_store.set("foo", token)

    print("\nSuccessfully set auth token.")
