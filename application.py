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
    # base_url="https://api.spoonacular.com/recipes/complexSearch"
    # payload = {
    #     'apiKey': spoonacular_api_key,
    #     'query': query,
    #     'instructionsRequire': True,
    #     'titleMatch': query,
    #     'number': 1
    # }
    # search_result = requests.get(base_url,params=payload)
    
    # recipe_id = search_result.json()['results'][0]['id']
    # return spooncular_request_recipe_id(recipe_id)
    result = {'vegetarian': True, 'vegan': False, 'glutenFree': False, 'dairyFree': True, 'veryHealthy': False, 'cheap': False, 'veryPopular': False, 'sustainable': False, 'weightWatcherSmartPoints': 12, 'gaps': 'no', 'lowFodmap': False, 'aggregateLikes': 4, 'spoonacularScore': 81.0, 'healthScore': 42.0, 'creditsText': 'Foodista.com – The Cooking Encyclopedia Everyone Can Edit', 'license': 'CC BY 3.0', 'sourceName': 'Foodista', 'pricePerServing': 137.24, 'extendedIngredients': [{'id': 16058, 'aisle': 'Canned and Jarred', 'image': 'chickpeas.png', 'consistency': 'solid', 'name': 'canned chickpeas', 'original': '540 ml can of chickpeas, drained and rinsed', 'originalString': '540 ml can of chickpeas, drained and rinsed', 'originalName': 'chickpeas, drained and rinsed', 'amount': 540.0, 'unit': 'ml', 'meta': ['drained and rinsed', 'canned'], 'metaInformation': ['drained and rinsed', 'canned'], 'measures': {'us': {'amount': 2.282, 'unitShort': 'cups', 'unitLong': 'cups'}, 'metric': {'amount': 540.0, 'unitShort': 'ml', 'unitLong': 'milliliters'}}}, {'id': 12698, 'aisle': 'Ethnic Foods;Health Foods', 'image': 'tahini-paste.png', 'consistency': 'solid', 'name': 'tahini', 'original': '2 tsp tahini', 'originalString': '2 tsp tahini', 'originalName': 'tahini', 'amount': 2.0, 'unit': 'tsp', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 2.0, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}, 'metric': {'amount': 2.0, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}}}, {'id': 1016168, 'aisle': 'Condiments', 'image': 'hot-sauce-or-tabasco.png', 'consistency': 'liquid', 'name': 'sriracha sauce', 'original': '½ tsp sriracha sauce', 'originalString': '½ tsp sriracha sauce', 'originalName': 'sriracha sauce', 'amount': 0.5, 'unit': 'tsp', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 0.5, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}, 'metric': {'amount': 0.5, 'unitShort': 'tsps', 'unitLong': 'teaspoons'}}}, {'id': 11215, 'aisle': 'Produce', 'image': 'garlic.png', 'consistency': 'solid', 'name': 'garlic', 'original': '3 cloves garlic', 'originalString': '3 cloves garlic', 'originalName': 'garlic', 'amount': 3.0, 'unit': 'cloves', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 3.0, 'unitShort': 'cloves', 'unitLong': 'cloves'}, 'metric': {'amount': 3.0, 'unitShort': 'cloves', 'unitLong': 'cloves'}}}, {'id': 11297, 'aisle': 'Produce;Spices and Seasonings', 'image': 'parsley.jpg', 'consistency': 'solid', 'name': 'fresh parsley', 'original': '3 tbsp fresh parsley, roughly chopped', 'originalString': '3 tbsp fresh parsley, roughly chopped', 'originalName': 'fresh parsley, roughly chopped', 'amount': 3.0, 'unit': 'tbsp', 'meta': ['fresh', 'roughly chopped'], 'metaInformation': ['fresh', 'roughly chopped'], 'measures': {'us': {'amount': 3.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}, 'metric': {'amount': 3.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}}}, {'id': 10011282, 'aisle': 'Produce', 'image': 'red-onion.png', 'consistency': 'solid', 'name': 'red onion', 'original': '¼ large red onion, diced', 'originalString': '¼ large red onion, diced', 'originalName': 'red onion, diced', 'amount': 0.25, 'unit': 'large', 'meta': ['diced', 'red'], 'metaInformation': ['diced', 'red'], 'measures': {'us': {'amount': 0.25, 'unitShort': 'large', 'unitLong': 'larges'}, 'metric': {'amount': 0.25, 'unitShort': 'large', 'unitLong': 'larges'}}}, {'id': 4042, 'aisle': 'Oil, Vinegar, Salad Dressing', 'image': 'peanut-oil.jpg', 'consistency': 'liquid', 'name': 'peanut oil', 'original': '4 tbsp peanut oil', 'originalString': '4 tbsp peanut oil', 'originalName': 'peanut oil', 'amount': 4.0, 'unit': 'tbsp', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 4.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}, 'metric': {'amount': 4.0, 'unitShort': 'Tbsps', 'unitLong': 'Tbsps'}}}, {'id': 11206, 'aisle': 'Produce', 'image': 'cucumber.jpg', 'consistency': 'solid', 'name': 'cucumber', 'original': '8 slices of cucumber', 'originalString': '8 slices of cucumber', 'originalName': 'cucumber', 'amount': 8.0, 'unit': 'slices', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 8.0, 'unitShort': 'slice', 'unitLong': 'slices'}, 'metric': {'amount': 8.0, 'unitShort': 'slice', 'unitLong': 'slices'}}}, {'id': 11529, 'aisle': 'Produce', 'image': 'tomato.png', 'consistency': 'solid', 'name': 'tomato', 'original': '8 slices of tomato', 'originalString': '8 slices of tomato', 'originalName': 'tomato', 'amount': 8.0, 'unit': 'slices', 'meta': [], 'metaInformation': [], 'measures': {'us': {'amount': 8.0, 'unitShort': 'slice', 'unitLong': 'slices'}, 'metric': {'amount': 8.0, 'unitShort': 'slice', 'unitLong': 'slices'}}}, {'id': 18350, 'aisle': 'Bakery/Bread', 'image': 'hamburger-bun.jpg', 'consistency': 'solid', 'name': 'hamburger buns', 'original': "4 hamburger buns (I used President's Choice multi-grain thins)", 'originalString': "4 hamburger buns (I used President's Choice multi-grain thins)", 'originalName': "hamburger buns (I used President's Choice multi-grain thins)", 'amount': 4.0, 'unit': '', 'meta': ["(I used President's Choice multi-grain thins)"], 'metaInformation': ["(I used President's Choice multi-grain thins)"], 'measures': {'us': {'amount': 4.0, 'unitShort': '', 'unitLong': ''}, 'metric': {'amount': 4.0, 'unitShort': '', 'unitLong': ''}}}, {'id': 93777, 'aisle': 'Milk, Eggs, Other Dairy', 'image': 'raita-or-tzaziki.png', 'consistency': 'solid', 'name': 'tzatziki', 'original': 'Tzatziki for topping', 'originalString': 'Tzatziki for topping', 'originalName': 'Tzatziki for topping', 'amount': 1.0, 'unit': 'serving', 'meta': ['for topping'], 'metaInformation': ['for topping'], 'measures': {'us': {'amount': 1.0, 'unitShort': 'serving', 'unitLong': 'serving'}, 'metric': {'amount': 1.0, 'unitShort': 'serving', 'unitLong': 'serving'}}}], 'id': 642539, 'title': 'Falafel Burger', 'readyInMinutes': 45, 'servings': 4, 'sourceUrl': 'https://www.foodista.com/recipe/DYNQRHMK/falafel-burger', 'image': 'https://spoonacular.com/recipeImages/642539-556x370.png', 'imageType': 'png', 'summary': 'You can never have too many middl eastern recipes, so give Falafel Burger a try. For <b>$1.37 per serving</b>, this recipe <b>covers 19%</b> of your daily requirements of vitamins and minerals. One portion of this dish contains around <b>12g of protein</b>, <b>20g of fat</b>, and a total of <b>402 calories</b>. This recipe serves 4. It is brought to you by Foodista. 4 people were impressed by this recipe. Head to the store and pick up onion, garlic, sriracha sauce, and a few other things to make it today. Only a few people really liked this main course. From preparation to the plate, this recipe takes about <b>about 45 minutes</b>. It is a good option if you\'re following a <b>dairy free and lacto ovo vegetarian</b> diet. With a spoonacular <b>score of 81%</b>, this dish is spectacular. Try <a href="https://spoonacular.com/recipes/clean-eating-falafel-burger-1063020">Clean eating falafel burger</a>, <a href="https://spoonacular.com/recipes/clean-eating-falafel-burger-848720">Clean eating falafel burger</a>, and <a href="https://spoonacular.com/recipes/falafel-veggie-burger-with-feta-yogurt-sauce-559036">Falafel Veggie Burger with Feta Yogurt Sauce</a> for similar recipes.', 'cuisines': ['Middle Eastern'], 'dishTypes': ['lunch', 'main course', 'main dish', 'dinner'], 'diets': ['dairy free', 'lacto ovo vegetarian'], 'occasions': [], 'winePairing': {'pairedWines': ['malbec', 'merlot', 'zinfandel'], 'pairingText': 'Burger works really well with Malbec, Merlot, and Zinfandel. Merlot will be perfectly adequate for a classic burger with standard toppings. Bolder toppings call for bolder wines, such as a malbec or peppery zinfandel. One wine you could try is Bodega Calle Alberti 154 Malbec. It has 4.3 out of 5 stars and a bottle costs about 13 dollars.', 'productMatches': [{'id': 450110, 'title': 'Bodega Calle Alberti 154 Malbec', 'description': 'Garnet violet color. Aromas of roasted nuts, latte, and dried berries with a supple, dry-yet-fruity medium body and a zesty, chocolate citrus peel, bacon bits, and earth accented finish with fine chewy tannins. Excellent balance and flavor for a wide range of foods.', 'price': '$12.99', 'imageUrl': 'https://spoonacular.com/productImages/450110-312x231.jpg', 'averageRating': 0.86, 'ratingCount': 5.0, 'score': 0.7975, 'link': 'https://click.linksynergy.com/deeplink?id=*QCiIS6t4gA&mid=2025&murl=https%3A%2F%2Fwww.wine.com%2Fproduct%2Fbodega-calle-alberti-154-malbec-2014%2F157179'}]}, 'instructions': 'Pat the chickpeas dry with a paper towel and throw them into a food processor along with the garlic.\nPuree until smooth.\nUsing your clean hands incorporate tahini, sriracha, parsley and onion into the chickpea mixture.\nForm mixture into four patties and set aside.\nHeat peanut oil in a large skillet over medium heat.\nOnce the oil begins to shimmer add the patties and cook for three minutes per side or until golden brown.\nRemove from and place in a hamburger bun.\nTop each burger with 2 slices of tomato, 2 slices of cucumber and a dollop of tzatziki.\nServe immediately.', 'analyzedInstructions': [{'name': '', 'steps': [{'number': 1, 'step': 'Pat the chickpeas dry with a paper towel and throw them into a food processor along with the garlic.', 'ingredients': [{'id': 16057, 'name': 'chickpeas', 'localizedName': 'chickpeas', 'image': 'chickpeas.png'}, {'id': 11215, 'name': 'garlic', 'localizedName': 'garlic', 'image': 'garlic.png'}], 'equipment': [{'id': 404771, 'name': 'food processor', 'localizedName': 'food processor', 'image': 'food-processor.png'}, {'id': 405895, 'name': 'paper towels', 'localizedName': 'paper towels', 'image': 'paper-towels.jpg'}]}, {'number': 2, 'step': 'Puree until smooth.', 'ingredients': [], 'equipment': []}, {'number': 3, 'step': 'Using your clean hands incorporate tahini, sriracha, parsley and onion into the chickpea mixture.', 'ingredients': [{'id': 16057, 'name': 'chickpeas', 'localizedName': 'chickpeas', 'image': 'chickpeas.png'}, {'id': 1016168, 'name': 'sriracha', 'localizedName': 'sriracha', 'image': 'hot-sauce-or-tabasco.png'}, {'id': 11297, 'name': 'parsley', 'localizedName': 'parsley', 'image': 'parsley.jpg'}, {'id': 12698, 'name': 'tahini', 'localizedName': 'tahini', 'image': 'tahini-paste.png'}, {'id': 11282, 'name': 'onion', 'localizedName': 'onion', 'image': 'brown-onion.png'}], 'equipment': []}, {'number': 4, 'step': 'Form mixture into four patties and set aside.', 'ingredients': [], 'equipment': []}, {'number': 5, 'step': 'Heat peanut oil in a large skillet over medium heat.', 'ingredients': [{'id': 4042, 'name': 'peanut oil', 'localizedName': 'peanut oil', 'image': 'peanut-oil.jpg'}], 'equipment': [{'id': 404645, 'name': 'frying pan', 'localizedName': 'frying pan', 'image': 'pan.png'}]}, {'number': 6, 'step': 'Once the oil begins to shimmer add the patties and cook for three minutes per side or until golden brown.', 'ingredients': [{'id': 4582, 'name': 'cooking oil', 'localizedName': 'cooking oil', 'image': 'vegetable-oil.jpg'}], 'equipment': [], 'length': {'number': 3, 'unit': 'minutes'}}, {'number': 7, 'step': 'Remove from and place in a hamburger bun.', 'ingredients': [{'id': 18350, 'name': 'hamburger bun', 'localizedName': 'hamburger bun', 'image': 'hamburger-bun.jpg'}], 'equipment': []}, {'number': 8, 'step': 'Top each burger with 2 slices of tomato, 2 slices of cucumber and a dollop of tzatziki.', 'ingredients': [{'id': 11206, 'name': 'cucumber', 'localizedName': 'cucumber', 'image': 'cucumber.jpg'}, {'id': 93777, 'name': 'tzatziki', 'localizedName': 'tzatziki', 'image': 'raita-or-tzaziki.png'}, {'id': 11529, 'name': 'tomato', 'localizedName': 'tomato', 'image': 'tomato.png'}], 'equipment': []}, {'number': 9, 'step': 'Serve immediately.', 'ingredients': [], 'equipment': []}]}], 'originalId': None, 'spoonacularSourceUrl': 'https://spoonacular.com/falafel-burger-642539'}
    return {'image':result['image'],'sourceUrl':result['sourceUrl'],'prepTime':result['readyInMinutes'],'extendedIngredients':result['extendedIngredients']}
   

ITEMS = 20
@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        food_name=request.form.get("food_name")
        tweet = twitter_search_request(food_name)
        recipe = spooncular_recipe_request(food_name)
        # f = open("recipe_result.txt", "a")
        # f.write(str(recipe))
        # f.close()
        return render_template("index.html",food_name=food_name,tweet=tweet,recipe=recipe)
    else:
        food_name = food_items[random.randint(0,len(food_items)-1)]
        tweet = twitter_search_request(food_name)
        recipe = spooncular_recipe_request(food_name)
        print(recipe['prepTime'])
        return render_template("index.html",food_name=food_name,tweet=tweet,recipe=recipe)
    
if __name__ == "__main__":
    app.run(
        debug=True,
        port=os.getenv("PORT",8080),
        host=os.getenv("IP","0.0.0.0")
    )