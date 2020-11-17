"""
    Controller logic defined here as well
    as setting up flask application on certain
    port is also defined here
"""
import os
import random
from flask import Flask, render_template, request, jsonify
from twitter_authentication import twitter_authentication
from twitter_queries import twitter_search_request
from spoonacular_api import (
    spoonacular_name_autocomplete,
    spoonacular_request_recipe_id,
    spoonacular_recipe_request,
)

APP = Flask(__name__)

KEY_FOOD_NAMES_ID_FILE = "food_names_with_id.txt"
KEY_FOOD_NAMES_HARDCODED_LIST = "food_list_hardcoded.txt"
ACCESS_TOKEN = twitter_authentication()


@APP.route("/", methods=["GET", "POST"])
def index():
    """
    When user visits the home page, render random recipe
    from harded coded list
    """
    if request.method == "POST":
        food_id = ""
        food_name = request.form.get("food_name")
        with open(KEY_FOOD_NAMES_ID_FILE, "r") as fin:
            food_items_id = eval(fin.read())
        for food_item_id, title in food_items_id.items():
            if title == food_name:
                food_id = food_item_id
        tweet = twitter_search_request(ACCESS_TOKEN, food_name)
        if food_id:
            recipe = spoonacular_request_recipe_id(food_id)
        else:
            recipe = spoonacular_recipe_request(food_name)
    elif request.method == "GET":
        with open(KEY_FOOD_NAMES_HARDCODED_LIST, "r") as fin:
            food_items = eval(fin.read())
        food_name = food_items[random.randint(0, len(food_items) - 1)]
        tweet = twitter_search_request(ACCESS_TOKEN, food_name)
        recipe = spoonacular_recipe_request(food_name)

    if len(recipe) == 1:
        return render_template("recipe_not_found.html", query=recipe)
    return render_template(
        "index.html", food_name=food_name, tweet=tweet, recipe=recipe
    )


@APP.route("/food_list")
def send_food_list():
    """
    send result of Spoonacular API autocomplete function to
    populate drop-down list for suggestion of food items
    """
    food_initials = request.args.get("a", type=str)
    food_items_id = {}
    response = []
    food_names = spoonacular_name_autocomplete(food_initials)
    for each in food_names:
        food_items_id[str(each["id"])] = each["title"]
        response.append(each["title"])
    with open(KEY_FOOD_NAMES_ID_FILE, "w") as fin:
        fin.write(str(food_items_id))
    return jsonify(response=response)


if __name__ == "__main__":
    APP.run(debug=True, port=os.getenv("PORT", 8080), host=os.getenv("IP", "0.0.0.0"))
