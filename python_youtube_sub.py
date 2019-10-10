#youtube gives the queries in json files
import json

#for text extraction (regular expressions)
import re

#making requests to urls
import urllib.requests

#So YouTube knows who is requesting (to throttle your requests)
api_key = "AIzaSyAGMq4k-PIhEsocN40SBovIk3TK8-USIMk"

#get request for the youtube data api
base_url = "https://www.googleapis.com/youtube/v3"
data_request = "/subscriptions?part=snippet&mySubscribers=true"
request = base_url+data_request

