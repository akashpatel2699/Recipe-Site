# Twitter API 

This application is created using **Python flask** (lightweight web framework), **Twitter API** to fetch random tweets based on random food item from a list of foods that is hard-coded in the program. 

## Requirements 

All the requirements that needs to be installed has been added to the requirements.txt that includes:
* python_dotenv (https://pypi.org/project/python-dotenv/)
* flask (https://flask.palletsprojects.com/en/1.1.x/)
* requests (https://requests.readthedocs.io/en/master/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

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
3. Create a file called **twitter.env** to store all the keys required for the Twitter API
using the command to create file:

```bash
touch twitter.env
```

4. Edit the file **twitter.env** using your favorite text-editor and entered the following lines:
    - export consumer_key="yourConsumerKey"
    - export consumer_secret="yourConsumerSecret"

3. Assuming installation step mentioned above has completed if not then run following command:

```bash
pip3 install -r requirements.txt
```

4. Finally run the application.py using:

```bash
python application.py
```

FAQ
---

Q: what if python is not installed on the system?

A: Go to [python website](https://www.python.org/) then Downloads on the menu bar to download for your system.

Q: where do I find my twitter consumer key and secret?

A: Follow the steps on the official website [Twitter Developer](https://developer.twitter.com/en/docs/getting-started)
