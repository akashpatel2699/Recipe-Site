"""
    All Spoonacular API requests defined here
"""
import os
from os.path import join, dirname
import requests
from dotenv import load_dotenv

SPOONACULAR_ENV = join(dirname(__file__), "spoonacular.env")
load_dotenv(SPOONACULAR_ENV)

SPOONACULAR_API_KEY = os.environ["SPOONACULAR_API_KEY"]

def spoonacular_name_autocomplete(substring):
    """
    Based on substring of food item being searched
    search for all that starts with that substring
    and return list of them. When API returns and
    error, return dictionary length of one
    """
    base_url = "https://api.spoonacular.com/recipes/autocomplete"
    payload = {"apiKey": SPOONACULAR_API_KEY, "query": substring, "number": 20}
    search_result = requests.get(base_url, params=payload)
    try:
        food_names = search_result.json()
    except IndexError:
        return {"query": substring}
    return food_names


def spoonacular_request_recipe_id(food_id):
    """
    Request recipe by id for full recipe information.
    When error return by API, return dict with length 1
    """
    base_url = "https://api.spoonacular.com/recipes/{}/information".format(food_id)
    payload = {"apiKey": SPOONACULAR_API_KEY, "includeNutritio": False}
    try:
        search_result = requests.get(base_url, params=payload)
        result = search_result.json()
        return {
            "title": result["title"],
            "image": result["image"],
            "sourceUrl": result["sourceUrl"],
            "prepTime": result["readyInMinutes"],
            "extendedIngredients": result["extendedIngredients"],
        }
    except (KeyError, IndexError):
        # returning dictionary wiht length 1 will show recipe not found
        return {"error on id": food_id}


def spoonacular_recipe_request(query):
    """
    Request for recipe based on food item but only care by food id
    that will be use to fetch actual recipe from API. On error,
    return dictionary of length 1
    """
    base_url = "https://api.spoonacular.com/recipes/complexSearch"
    payload = {
        "apiKey": SPOONACULAR_API_KEY,
        "query": query,
        "instructionsRequire": True,
        "titleMatch": query,
        "number": 1,
    }
    search_result = requests.get(base_url, params=payload)
    try:
        recipe_id = search_result.json()["results"][0]["id"]
    except (IndexError, KeyError):
        # returning dictionary wiht length 1 will show recipe not found
        return {"query": query}
    return spoonacular_request_recipe_id(recipe_id)
