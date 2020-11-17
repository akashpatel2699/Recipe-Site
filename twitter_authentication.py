"""
    Twitter Authentication using consumer key and consumer secret
"""
import os
import base64
import requests
from dotenv import load_dotenv
from os.path import join, dirname

twitter_env = join(dirname(__file__),'twitter.env')
load_dotenv(twitter_env)

consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']

TWITTER_BASE_URL = 'https://api.twitter.com/'

def twitter_authentication():
    # base64 Encoding of two key into one for Twitter API Authentication
    key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    
    twitter_auth_url = '{}oauth2/token'.format(TWITTER_BASE_URL)
    
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    
    auth_data = {
        'grant_type': 'client_credentials'
    }
    # POST request to obtain Bearer Token (access key)
    auth_resp = requests.post(twitter_auth_url, headers=auth_headers, data=auth_data)
    
    return auth_resp.json()['access_token']