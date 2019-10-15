'''
NOTE:
	Instagram does not require credentials to request user data
'''



#importing request libraries for website query
import requests


#edpoint url
url = "https://www.instagram.com/"
username = "nasa" #i like pictures of space
query = "/?__a=1"

request_url = url+username+query

response = requests.get(request_url)

#method json() converts the payload to a readable dictionary format
data = response.json()

#data contains all the account information for specified username
#tree structure is useful to visualize where we are
'''
logging_page_id ->
show_suggester_profiles ->
show_follow_dialog ->
graphql -->
		|
		|-->user -->
				 |
				 |--> edge_followed_by -->
				 						|
										|-->count
'''

print(username, " follower count: ", data['graphql']['user']['edge_followed_by']['count'])

