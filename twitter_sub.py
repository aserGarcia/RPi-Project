#pip3 install python-twitter
#Twython is a twitter api wrapper for python, allows easy access
from twython import Twython

#api_credentials
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""

#creating object of class Twython
twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

#veryfy_credentials returns metadata from the user's account, including their follower count
#https://developer.twitter.com/en/docs/accounts-and-users/manage-account-settings/api-reference/get-account-verify_credentials
#https://twython.readthedocs.io/en/latest/usage/basic_usage.html#user-information
response = twitter.verify_credentials()
print(response["followers_count"])


#showing IronMan follower's count
response1 = twitter.show_user(screen_name="RobertDowneyJr")
print(response1["followers_count"])
