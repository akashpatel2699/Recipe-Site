# Twitter API 

This application is created using **Python flask** (lightweight web framework), **Twitter API** to 
fetch random tweets based on a random food item from a list of foods that is hard-coded in the program. 

## Requirements 

All the requirements that needs to be installed has been added to the requirements.txt that includes:
* [python_dotenv](https://pypi.org/project/python-dotenv/) - useful for loading environment variables
* [flask](https://flask.palletsprojects.com/en/1.1.x/) - Python micro web-framework
* [requests](https://requests.readthedocs.io/en/master/) - Python HTTP library useful for making API Calls 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages assuming
you have the lastest version of pip installed that is pip3. If not then use pip instead.

```bash
pip3 install -r requirements.txt
```

## Usage 

1. Clone the repository using git command clone as follow:

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

8. Assuming installation step mentioned above has completed if not then run following command:

```bash
pip3 install -r requirements.txt
```

9. Finally run the application.py using:

```bash
python application.py
```

10. If on *Cloud9*, preview templates/index.html. This should successfully render the HTML! 

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

##### Known Issues
* I could have styled the page a bit better than current style.

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