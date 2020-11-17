"""
    Search Twitter Quotes
"""
import os
import random
import requests
from time import strftime, strptime
from twitter_authentication import twitter_authentication

TWITTER_BASE_URL = 'https://api.twitter.com/'

def twitter_search_request(querry):
    COUNT = 20

    #Search Query to be send to fetch some data from Twitter API endpoint
    search_headers = {
        'Authorization': 'Bearer {}'.format(twitter_authentication())    
    }
    #Options for search parameters 
    search_params = {
        'q': '{}'.format(querry),
        'result_type': 'recent',
        'lang': 'en',
        'tweet_mode': 'extended',
        'count': COUNT
    }
    
    search_url = '{}1.1/search/tweets.json'.format(TWITTER_BASE_URL)
    
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    
    tweet_data = search_resp.json()
    #select random tweet from fetched tweets
    try:
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
    except: 
        twitter_search_request("best food")