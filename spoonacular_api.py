"""
    All Spoonacular API requests defined here
"""
import os 
import requests
from dotenv import load_dotenv
from os.path import join, dirname

spoonacular_env = join(dirname(__file__),'spoonacular.env')
load_dotenv(spoonacular_env)

spoonacular_api_key=os.environ['spoonacular_api_key']

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