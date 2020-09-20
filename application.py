from flask import Flask, render_template, request
import os
import random
from dotenv import load_dotenv
import base64
import requests
from time import strftime, strptime

#Load all environments variables 
# set as system variables
load_dotenv()

app=Flask(__name__)

consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']
spoonacular_api_key=os.environ['spoonacular_api_key']

# base64 Encoding of two key into one for Twitter API Authentication
key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}
# POST request to obtain Bearer Token (acces key)
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

access_token = auth_resp.json()['access_token']

food_items = [
    "Pasta",
    "Mexican Pizza",
    "Biryani",
    "Pani Puri",
    "Falafal",
    "Sandwich",
    "Dosa"
    ]

def twitter_search_request(querry):
    COUNT = 20
    random_food_index = random.randint(0,len(food_items)-1)
    random_tweet_index = random.randint(0,COUNT-1)
    #Search Query to be send to fetch some data from Twitter API endpoint
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    #Options for search parameters 
    search_params = {
        'q': '{}'.format(querry),
        'result_type': 'recent',
        'lang': 'en',
        'count': COUNT
    }
    
    search_url = '{}1.1/search/tweets.json'.format(base_url)
    
    search_resp = requests.get(search_url, headers=search_headers, params=search_params)
    
    tweet_data = search_resp.json()
    
    for status in tweet_data['statuses']:
        if (random_tweet_index) == random_food_index:
            tweet = status
            break
        elif random_tweet_index < random_food_index:
            random_tweet_index += 1
        else:
            random_tweet_index -= 1
    tweet['created_at'] = strftime("%a, %d %b %H:%M:%S %Y",strptime(tweet['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))
    return tweet

def spooncular_request_recipe_id(id):
    base_url="https://api.spoonacular.com/recipes/{}/information".format(id)
    payload = {
        'apiKey': spoonacular_api_key,
        'includeNutritio': False
    }
    search_result = requests.get(base_url,params=payload)
    recipes = search_result.json()
    return recipes
    
def spooncular_recipe_request(query):
    base_url="https://api.spoonacular.com/recipes/complexSearch"
    payload = {
        'apiKey': spoonacular_api_key,
        'query': query,
        'instructionsRequire': True,
        'titleMatch': query,
        'number': 1
    }
    search_result = requests.get(base_url,params=payload)
    
    recipe_id = search_result.json()['results'][0]['id']
    return spooncular_request_recipe_id(recipe_id)
   

ITEMS = 20
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        food_name=request.form.get("food_name")
        tweet = twitter_search_request(food_name)
        recipe = spooncular_recipe_request(food_name)
        f = open("recipe_result.txt", "a")
        f.write(str(recipe))
        f.close()
        return render_template("index.html",food_name=food_name,tweet=tweet)
    else:
        food_name = food_items[random.randint(0,len(food_items)-1)]
        tweet = twitter_search_request(food_name)
        return render_template("index.html",food_name=food_name,tweet=tweet)
    
if __name__ == "__main__":
    app.run(
        debug=True,
        port=os.getenv("PORT",8080),
        host=os.getenv("IP","0.0.0.0")
    )