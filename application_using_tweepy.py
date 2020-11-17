from flask import Flask, render_template, request
from tweepy import OAuthHandler, API, Cursor
import os
import random
from dotenv import load_dotenv

# Load all environments variables
# set as system variables
load_dotenv()

app = Flask(__name__)

consumer_key = os.environ["consumer_key"]
consumer_secret = os.environ["consumer_secret"]
access_token = os.environ["access_token"]
access_token_secret = os.environ["access_token_secret"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

food_items = [
    "Pasta",
    "Mexican Pizza",
    "Biryani",
    "Pani Puri",
    "Falafal",
    "Sandwich",
    "Dosa",
]


def make_search_request(food_name):
    random_food = random.randint(0, len(food_items) - 1)
    random_tweet = random.randint(0, ITEMS - 1)
    for status in Cursor(auth_api.search, q=food_name, lang="en").items(ITEMS):
        if (random_tweet) == random_food:
            tweet = status
            break
        elif random_tweet < random_food:
            random_tweet += 1
        else:
            random_tweet -= 1
    return tweet


ITEMS = 20


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        food_name = request.form.get("food_item")
        tweet = make_search_request(food_name)
        return render_template("index.html", food_name=food_name, tweet=tweet)
    else:
        food_name = food_items[random.randint(0, len(food_items) - 1)]
        tweet = make_search_request(food_name)
        return render_template("index.html", food_name=food_name, tweet=tweet)


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", 8080), host=os.getenv("IP", "0.0.0.0"))
