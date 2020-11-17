import os
import random
import base64
import requests
from dotenv import load_dotenv
from os.path import join, dirname
from time import strftime, strptime
from flask import Flask, render_template, request, jsonify
from twitter_queries import twitter_search_request
from spoonacular_api import spooncular_name_autocomplete, spooncular_request_recipe_id\
    ,spooncular_recipe_request

app=Flask(__name__)

KEY_FOOD_NAMES_ID_FILE = "food_names_with_id.txt"
KEY_FOOD_NAMES_HARDCODED_LIST = "food_list_hardcoded.txt"

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