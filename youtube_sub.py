#importing youtube data api libraries
#documentation at: https://youtube-data-api.readthedocs.io/en/latest/index.html
from youtube_api import YouTubeDataAPI

#So YouTube knows who is requesting (to throttle your requests)
#It is important to not disclose your apiKey or else anyone can make requests on your behalf
api_key = ""

#Initialize an object of class YouTubeDataAPI to
#access api functionality

#The API key is the argument, if you do not have one it will throw an error
yt = YouTubeDataAPI(api_key)

#the channel id is unique to every channel, we need it for getting data later
pew_channel_id = yt.get_channel_id_from_user('PewDiePie')

#request channel data
channel_data = yt.get_channel_metadata(pew_channel_id)


#printing out the data (first is dictionary, second is sub count)
print(channel_data)
print(channel_data['subscription_count'])
