# Recipe Site Using Twitter and Spoonacular APIs

This application is created using **Python flask** (lightweight web framework), **Twitter API** to 
fetch random tweets based on a random food item or searched food item and fetch recipe information 
using **Spoonacular API** to be displayed on the screen.

## Requirements 

All the requirements that needs to be installed has been added to the requirements.txt that includes:
* [python_dotenv](https://pypi.org/project/python-dotenv/) - useful for loading environment variables
* [flask](https://flask.palletsprojects.com/en/1.1.x/) - Python micro web-framework
* [requests](https://requests.readthedocs.io/en/master/) - Python HTTP library useful for making API Calls 
* [heroku](https://devcenter.heroku.com/categories/python-support) - Cloud based web hosting for **FREE**

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages assuming
you have the lastest version of pip installed that is pip3. If not then use pip instead.

```bash
pip3 install -r requirements.txt
```

## Usage 

1. If **git** is not installed, then follow on [git website](https://git-scm.com/) to get started.
Then, Clone the repository using git command clone as follow:

```bash    
git clone https://github.com/NJIT-CS490/project1-amp228.git
```

2. Go to that directory or folder using cd

```bash   
cd project1
```

3. Sign up for the [twitter developer portal](https://developer.twitter.com )

4. Navigate to [https://developer.twitter.com/en/portal/projects-and-apps](https://developer.twitter.com/en/portal/projects-and-apps).
    Make a new app.

5. Click on the *key symbol* after creating your project, and it will take you to your keys and tokens.
    If needed, you can regenerate your access token and secret.

6. Create a file called **twitter.env** to store all the keys required for the Twitter API
using the command to create file:

```bash
touch twitter.env
```

7. Edit the file **twitter.env** using your favorite text-editor and entered the following lines.
Find more information on how to get your keys on the bottom in **FAQ** section.
    - export consumer_key="yourConsumerKey"
    - export consumer_secret="yourConsumerSecret"

8. Sign up for [spoonacular api](https://spoonacular.com/food-api/console#Dashboard)

9. After log in to your dashboard, click *profile* and then toggle **Show/Hide API Key** button

10. Create a file called **spoonacular.env** to store all the keys required for the Spoonacular
API using the command to create file:

```bash
touch spoonacular.env
```

11. Edit the file **spoonacular.env** using your favorite text-editor and once opened enter following liens.
    - export spoonacular_api_key="yourAPIKey"

12. Assuming installation step mentioned above has completed if not then run following command:

```bash
pip3 install -r requirements.txt
```

13. Finally run the application.py using:

```bash
python application.py
```

14. If on *Cloud9*, preview templates/index.html. This should successfully render the HTML! 

15. If you like to deploy to your **git repository**, then follow these steps:

    - Go to your git profile and then *create* a new repository 
    - Create a file called **.gitignore** to hide your keys from pushing 
    to your git repository using next few steps:
    ```bash
    touch .gitignore
    echo "twitter.env" >> .gitignore
    echo "spoonacular.env" >> .gitignore
    ```
    - Then copy the line where it says git remote set-url origin yourResopURL
```bash
git remote add origin https://github.com/<your-username>/<repository-name>.git
git branch -M master
git push -u origin master
```
16. If you want to deploy your application on free web-hosting servers; then 
follow next couple of steps:
    1. Create [heroku](https://signup.heroku.com/) account 
    2. Create a file called **Procfile** and open using your text-editor to insert
    **web: python application.py**, then close the file
    3. Back to your computer/terminal then type to login using your credential
    through terminal to be deploy:
    ```bash
    heroku login -i
    heroku create
    git push heroku master
    ```
    4. Now go to your **heroku** dashboard and then select the recently created app  
    5. Go to **settings**, then click **Reveal Config Vars** 
    6. Then fill in the key value pairs as shown below:
        - consumer_key="yourConsumerKey Is your value"
        - consumer_secret="yourConsumerSecret Is your value"
        - spoonacular_api_key="yourAPIKey Is your value"

## Useful Package

* [tweepy](http://docs.tweepy.org/en/latest/getting_started.html) -
easy-to-use Python library for accessing the Twitter API

## Issues

##### Technical Issues
* First technical issue had to do with style.css so after editing style.css I had to restart
the application or hard refreshing using
*Ctrl+Shift+R* on Windows and *Command+Shift+R* on Macos for style updates to be displayed.

* Second technical issue had to do with selecting random tweet from fetched Twitter data. 
I was using bunch of variables to return random tweet after fetching the data, but later I learned from **Slack** 
to use random.choice() instead.

* I had trouble getting autocomplete working and finding a fix for the issue.  

##### Known Issues
* If I had more time, I could have made my website little more responsive and better design. I might have also fixed a jquery issue 
where it adds white space on the bottom of the page when autocomplete is trigged after 4 character typed in the input field\.

FAQ
---

Q: what if python is not installed on the system?

A: Go to [python website](https://www.python.org/) then Downloads on the menu bar to download for your system.

---

Q: What if I need more assitance signing up for twitter developer account?

A: Follow these steps on the official website [Twitter Developer](https://developer.twitter.com/en/docs/getting-started)

---

Q: Do I need to install **pip**?

A: pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from [python.org](https://www.python.org/). 

---

Q: What if I need more help either deploying or troubleshooting my app on **heroku**?

A: Follow this [article](https://devcenter.heroku.com/articles/git) to get more help

---

Q: Where to find more help with **Spoonacular API**?

A: Follow [Spoonacular API](https://spoonacular.com/food-api/docs) documentation for that.