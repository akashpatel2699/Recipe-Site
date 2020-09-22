import os
import random
import base64
import requests
from dotenv import load_dotenv
from os.path import join, dirname
from time import strftime, strptime
from flask import Flask, render_template, request

#Load all environments variables 
# set as system variables
twitter_env = join(dirname(__file__),'twitter.env')
load_dotenv(twitter_env)

app=Flask(__name__)

twitter_consumer_key=os.environ['consumer_key']
twitter_consumer_secret=os.environ['consumer_secret']

# base64 Encoding of two key into one for Twitter API Authentication
key_secret = '{}:{}'.format(twitter_consumer_key, twitter_consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

twitter_base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(twitter_base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}
# POST request to obtain Bearer Token (acces key)
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

# Access Token recieved back from authentication response
access_token = auth_resp.json()['access_token']

food_items = [
    "Pasta",
    "Samosa",
    "Biryani",
    "Pani Puri",
    "Falafal",
    "Sandwich",
    "Dosa"
    ]

def twitter_search_request(querry):
    COUNT = 20
    #Search Query to be send to fetch some data from Twitter API endpoint
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    #Options for search parameters 
    search_params = {
        'q': '{}'.format(querry),
        'result_type': 'recent',
        'lang': 'en',
        'tweet_mode': 'extended',
        'count': COUNT
    }
    
    search_url = '{}1.1/search/tweets.json'.format(twitter_base_url)
    
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    
    tweet_data = search_resp.json()
    
    #select random tweet from fetched tweets
    tweet = random.choice(tweet_data['statuses'])
    try:
        # if the tweet is a retweet then I want the full text if availabe
        tweet['full_text'] = tweet['retweeted_status']['full_text']
    except KeyError:
        # if the tweet is not a retweet then just full text
        tweet['full_text'] = tweet['full_text']
   
    #format datetime to remove +000 from it
    tweet['created_at'] = strftime("%a, %d %b %H:%M:%S %Y",strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))

    return {'text':tweet['full_text'],'username':tweet['user']['name'],'created_at':tweet['created_at']}

@app.route("/")
def index():
        food_name = food_items[random.randint(0,len(food_items)-1)]
        tweet = twitter_search_request(food_name)
        return render_template("index.html",food_name=food_name,tweet=tweet)
    
if __name__ == "__main__":
    app.run(
        debug=True,
        port=os.getenv("PORT",8080),
        host=os.getenv("IP","0.0.0.0")
    )