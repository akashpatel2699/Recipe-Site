import os
import random
import base64
import requests
from dotenv import load_dotenv
from os.path import join, dirname
from time import strftime, strptime
from flask import Flask, render_template, request, jsonify


#Load all environments variables 
# set as system variables
twitter_env = join(dirname(__file__),'twitter.env')
load_dotenv(twitter_env)

spoonacular_env = join(dirname(__file__),'spoonacular.env')
load_dotenv(spoonacular_env)

app=Flask(__name__)

consumer_key=os.environ['consumer_key']
consumer_secret=os.environ['consumer_secret']
spoonacular_api_key=os.environ['spoonacular_api_key']
twitter_base_url = 'https://api.twitter.com/'
KEY_FOOD_NAMES_ID_FILE = "food_names_with_id.txt"
KEY_FOOD_NAMES_HARDCODED_LIST = "food_list_hardcoded.txt"

def twitter_authentication():
    # base64 Encoding of two key into one for Twitter API Authentication
    key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    
    twitter_auth_url = '{}oauth2/token'.format(twitter_base_url)
    
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
    
    search_url = '{}1.1/search/tweets.json'.format(twitter_base_url)
    
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

def spooncular_name_autocomplete(substring):
    base_url="https://api.spoonacular.com/recipes/autocomplete"
    payload = {
        'apiKey': spoonacular_api_key,
        'query': substring,
        'number': 20
    }
    search_result = requests.get(base_url,params=payload)
    try:
        food_names = search_result.json()
    except IndexError:
        return {'query':substring}
    return food_names

def spooncular_request_recipe_id(id):
    base_url="https://api.spoonacular.com/recipes/{}/information".format(id)
    payload = {
        'apiKey': spoonacular_api_key,
        'includeNutritio': False
    }
    search_result = requests.get(base_url,params=payload)
    result = search_result.json()
    return {'title':result['title'],
        'image':result['image'],
        'sourceUrl':result['sourceUrl'],
        'prepTime':result['readyInMinutes'],
        'extendedIngredients':result['extendedIngredients']
    }
    
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
    try:
        recipe_id = search_result.json()['results'][0]['id']
    except IndexError:
        return {'query':query}
    return spooncular_request_recipe_id(recipe_id)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        food_id = ''
        food_names_id = {}
        food_name=request.form.get("food_name")
        # TODO need food id if in food_names_id
        with open(KEY_FOOD_NAMES_ID_FILE,"r") as fin:
            food_items_id = eval(fin.read())
        for id, title in food_items_id.items():
            if (title == food_name):
                food_id = id
        tweet = twitter_search_request(food_name)
        if(food_id):
            recipe = spooncular_request_recipe_id(food_id)
        else:
            recipe = spooncular_recipe_request(food_name)
        if len(recipe) == 1:
            return render_template("recipe_not_found.html",query=recipe)
        return render_template("index.html",food_name=food_name,tweet=tweet,recipe=recipe)
    else:
        with open(KEY_FOOD_NAMES_HARDCODED_LIST,"r") as fin:
            food_items = eval(fin.read())
        food_name = food_items[random.randint(0,len(food_items)-1)]
        tweet = twitter_search_request(food_name)
        recipe = spooncular_recipe_request(food_name)
        if len(recipe) == 1:
            return render_template("recipe_not_found.html",query=recipe)
        return render_template("index.html",food_name=food_name,tweet=tweet,recipe=recipe)
        
@app.route("/food_list")
def send_food_list():
    food_initials = request.args.get('a',type=str)
    food_items_id = {}
    response = []
    food_names = spooncular_name_autocomplete(food_initials)
    for each in food_names:
        food_items_id[str(each['id'])] = each['title']
        response.append(each['title'])
    with open(KEY_FOOD_NAMES_ID_FILE,"w") as fin:
        fin.write(str(food_items_id))
    return jsonify(response=response)
    
if __name__ == "__main__":
    app.run(
        debug=True,
        port=os.getenv("PORT",8080),
        host=os.getenv("IP","0.0.0.0")
    )