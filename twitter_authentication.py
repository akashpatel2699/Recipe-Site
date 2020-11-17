"""
    Twitter Authentication using consumer key and consumer secret
"""
import os
import base64
from os.path import join, dirname
import requests
from dotenv import load_dotenv

TWITTER_ENV = join(dirname(__file__), "twitter.env")
load_dotenv(TWITTER_ENV)

CONSUMER_KEY = os.environ["consumer_key"]
CONSUMER_SECRET = os.environ["consumer_secret"]

TWITTER_BASE_URL = "https://api.twitter.com/"

def twitter_authentication():
    """
    base64 Encoding of two key into one for Twitter API Authentication
    using Consumer key and consumer secret authenticate with Twitter
    """
    key_secret = "{}:{}".format(CONSUMER_KEY, CONSUMER_SECRET).encode("ascii")
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode("ascii")

    twitter_auth_url = "{}oauth2/token".format(TWITTER_BASE_URL)

    auth_headers = {
        "Authorization": "Basic {}".format(b64_encoded_key),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

    auth_data = {"grant_type": "client_credentials"}

    auth_resp = requests.post(twitter_auth_url, headers=auth_headers, data=auth_data)

    return auth_resp.json()["access_token"]
