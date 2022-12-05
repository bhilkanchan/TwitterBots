# Twitter-Bots
Twitter bots to follow and message users, like tweets and retweet written in python.


## Table of Contents
+ [Technologies Used](https://github.com/bhilkanchan/Twitter-Bots/blob/main/README.md#technologies-used)
+ [Local Setup](https://github.com/bhilkanchan/Twitter-Bots/blob/main/README.md#local-setup)
+ [ToDo](https://github.com/bhilkanchan/Twitter-Bots/blob/main/README.md#to-do)


## Technologies Used
+ Tweepy
+ Python


## Local setup
1. Create virtual environment to install libraries
```
python -m venv venv
```
2. Activate the virtual environment
```
venv\Scripts\activate
```
3. Install all dependencies
```
pip install -r requirements.txt
```
4. Add your API key, API key secret, access token and access token secret in .env file
5. Add Google Sheet credentials in gsheet_credentials.json
6. Customize the fields in allbots.py
7. Run the file
```
python allbots.py
```


## ToDo
+ Add steps and files to deploy the bot file to heroku
