import tweepy
import time
import os
import gspread
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# Add all the values of the bot account in .env file
API_KEY = os.environ["API_KEY"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Add values in gsheet_credentials.json file
gc = gspread.service_account(filename='gsheet_credentials.json')
sh = gc.open('Receiver_ids')
worksheet1 = sh.worksheet("Sheet1")
res1 = worksheet1.get_all_records()

countfollow = 0
countmessage = 0
requestcount = 0
countunfollow = 0
countlike = 0
countretweet = 0
countaddmessage = 0

# Add your username here
myusername = "" 
# Customize the message
messagetext = "Hey" 
# Add your screen name here
myid = api.get_user(screen_name='')

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

# Follow and message users who tweet in a specific area
def follow_message(querytext, geocodetext):
    global countmessage
    global countfollow
    global requestcount
    idlist1 = list(res1)
    # Use cursor to divide the results in 100 per page
    cursor = tweepy.Cursor(api.search_tweets, q=querytext, geocode=geocodetext)
    for page in cursor.pages(20):
        for tweet in page:
            try:
                if(requestcount <= 99000):
                    # Get the friendship status between you and the user
                    friendship = api.get_friendship(source_screen_name=myusername, target_screen_name=tweet.user.screen_name)
                    requestcount = requestcount+1

                    # Check that you are not following the user and user's messaging option is open
                    if(friendship[0].following == False and countfollow <= 950 and friendship[0].can_dm == True and str(tweet.user.id) not in idlist1):
                        api.create_friendship(screen_name=tweet.user.screen_name)
                        requestcount = requestcount+1

                        print("Request count is:", requestcount)
                        print("followed:", tweet.user.screen_name)
                        
                        countfollow = countfollow+1
                        print('Follow count:', countfollow)

                        api.send_direct_message(recipient_id=tweet.user.id, text=messagetext)
                        requestcount = requestcount+1

                        print("Request count is:", requestcount)
                        print("sent message to:", tweet.user.screen_name)

                        countmessage = countmessage+1
                        print('Message count:', countmessage)

                        next_row = next_available_row(worksheet1)
                        # Append the userid in Google Sheet
                        worksheet1.update_acell("A{}".format(next_row), tweet.user.id_str)
                        idlist1.append(tweet.user.id_str)
                        print("Added user id to txt file and list")
                    time.sleep(20)
                else:
                    break
            except tweepy.HTTPException as e:
                print(e)
                if(e.api_codes == 226):
                    time.sleep(600)
                else:
                    time.sleep(5)


# Like the tweets of users with specific words
def like_tweet(querytext):
    global countlike
    global requestcount
    for tweet in api.search_tweets(q=querytext):
        try:
            if(requestcount <= 99000):
                tweetid = api.get_status(tweet.id)
                requestcount = requestcount+1
                if(tweetid.favorited == False and countlike < 950):
                    api.create_favorite(tweet.id)
                    requestcount = requestcount+1
                    print("Request count is:", requestcount)
                    print("Liked tweet of user:", tweet.user.screen_name)
                    countlike = countlike+1
                    print('Tweet like count:', countlike)
                time.sleep(30)
            else:
                break
        except tweepy.HTTPException as e:
            print(e)
            if(e.api_codes == 226):
                time.sleep(600)
            else:
                time.sleep(5)


# Retweet the tweets of users with specific words
def re_tweet(querytext):
    global countretweet
    global requestcount
    for tweet in api.search_tweets(q=querytext):
        try:
            if(requestcount <= 99000):
                setretweeted = api.get_status(tweet.id)
                requestcount = requestcount+1
                if(setretweeted.retweeted == False and countretweet < 950):
                    api.retweet(tweet.id)
                    requestcount = requestcount+1
                    print("retweeted", tweet.id)
                    countretweet = countretweet+1
                time.sleep(60)
            else:
                break
        except tweepy.HTTPException as e:
            print(e)
            if(e.api_codes == 226):
                time.sleep(600)
            else:
                time.sleep(5)


# Unfollow user
def unfollow_user():
    global countmessage
    global countunfollow
    global requestcount
    cursor = tweepy.Cursor(api.get_friend_ids, screen_name=myusername, count=5000)
    for page in cursor.pages(50):
        for tweet in page:
            try:
                if(requestcount <= 99990):
                    usercheck = api.get_user(user_id=tweet)
                    friendship = api.get_friendship(source_screen_name=myusername, target_screen_name=usercheck.screen_name)
                    print(usercheck.screen_name, "Follows me?", friendship[1].following)
                    requestcount = requestcount+2
                    if(friendship[1].following == False):
                        api.destroy_friendship(screen_name=usercheck.screen_name)
                        countunfollow = countunfollow+1
                        requestcount = requestcount+1
                        print("Request count is:", requestcount)
                        print("Unfollowed:", usercheck.screen_name)
                    time.sleep(20)
                else:
                    break
            except tweepy.HTTPException as e:
                print(e)
                if(e.api_codes == 226):
                    time.sleep(600)
                else:
                    time.sleep(5)


# Add message related information in Google sheet to analyse/keep track of the messages
def add_messages():
    worksheet2 = sh.worksheet("Sheet2")
    res2 = worksheet2.col_values(1)
    global countaddmessage
    cursor = tweepy.Cursor(api.get_direct_messages)  
    for page in cursor.pages(50):
        for message in page:
            try:
                idlist2 = list(res2)
                if(requestcount <= 99990 and message.message_create['sender_id'] not in idlist2):
                    next_row = next_available_row(worksheet2)
                    worksheet2.update_acell("A{}".format(next_row), message.message_create['sender_id'])
                    sender = api.get_user(user_id=message.message_create['sender_id'])
                    worksheet2.update_acell("B{}".format(next_row), sender.screen_name)
                    worksheet2.update_acell("C{}".format(next_row), message.message_create['message_data']['text'])
                    countaddmessage = countaddmessage+1
                    print(countaddmessage)
                    time.sleep(5)
                else:
                    break
            except tweepy.HTTPException as e:
                print(e)
                if(e.api_codes == 226):
                    time.sleep(600)


def main():
    add_messages()
    # Geocode of New York is added here, change the geocode to your required place
    follow_message(" ", "40.730610,-73.935242,5mi")
    time.sleep(300)


if __name__ == "__main__":
    main()


# Insert query to like the tweet
like_tweet("")
time.sleep(100)

# Insert query to retweet the tweet
re_tweet("")
time.sleep(100)


if(myid.friends_count > 4200):
    unfollow_user()
    print("Unfollowed:", countunfollow, date.today())

print("message count:", countmessage, date.today())
print("follow count:", countfollow, date.today())
print("Like count:", countlike, date.today())
print("retweet count:", countretweet, date.today())
print("unfollowed:", countunfollow, date.today())
print("Added replies:", print(countaddmessage), date.today())



