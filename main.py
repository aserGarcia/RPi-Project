#for data
import requests
from twython import Twython
from youtube_api import YouTubeDataAPI

#for screen
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

#for LED
import neopixel


class SubCount:

	def __init__(self, account_dict, credentials_dict, images, font_file_path='default'):
		'''
		Constructor for the SubCount object
		@param: account_dict - dictionary of social 
				network/account
				Ex.) 
				{'Twitter': 'Robert Downey Jr', 'YouTube': 'Pewdiepie'}
		@param: credentials_dict - dictionary of credentials for APIs
		@param: images - list of images/image path(s) to make animation/display
		@param: font_file_path - file path to font for display (format .ttf)
		'''
		self.IMAGE_DIMENSIONS = (128, 64) #(width, height)

		self.account_dict = account_dict
		self.images = images
		if font_file_path=='default':
			self.font = ImageFont.load_default()			
		else:
			self.font = ImageFont.truetype(font_file_path)
		
		#trying social medial credentials
		try:
			self.twAPI_KEY, self.twAPI_SECRET, self.twACCESS_TOKEN, self.twACCESS_SECRET = credentials_dict['Twitter']
			self.twitter = Twython(self.twAPI_KEY, self.twAPI_SECRET,
								 self.twACCESS_TOKEN, self.twACCESS_SECRET)
		except KeyError:
			print('Error Twitter Credentials...')
			pass

		try:
			self.youtube = YouTubeDataAPI(credentials_dict['YouTube'])
		except KeyError:
			print('Error YouTube Credentials...')
			pass

		#use I2C
		i2c = board.I2C()
		#define reset pin
		oled_reset = digitalio.DigitalInOut(board.D4)
		self.oled = adafruit_ssd1306.SSD1306_I2C(self.IMAGE_DIMENSIONS[0], self.IMAGE_DIMENSIONS[1], i2c, addr=0x3c, reset=oled_reset)

	def update_account_dict(self, account_dict):
		'''
		@param: account_dict to replace old ones
		'''
		if len(account_dict) == 0:
			print('account dictionary must not be empty.')
		else:
			self.account_dict = account_dict
			print('updated account dictionary')
	
	def update_images(self, images):
		'''
		@param: images - images to replace old ones
		'''
		if len(images) == 0:
			print('images list is empty')
		else:
			self.images = images
			print('updated images')

	def get_twitter_subscribers(self, account=None):
		'''
		Get account data from twitter
		@param: account_dict - default None (uses currently stored information)
		@return: twitter sub data
		'''

		if account != None:
			self.account_dict['Twitter'] = account
		response = self.twitter.show_user(screen_name=self.account_dict['Twitter'])
		return response["followers_count"]

	def get_youtube_subscribers(self, account=None):
		if account != None:
			self.account_dict['Youtube'] = account
		channel_id = self.youtube.get_channel_id_from_user(self.account_dict['YouTube'])
		channel_data = self.youtube.get_channel_metadata(channel_id)
		return channel_data['subscription_count']

	def get_intagram_subscribers(self, account=None):
		url = "https://www.instagram.com/"
		query = "/?__a=1"
		if account != None:
			self.account_dict['Instagram'] = account
		request_url = url+self.account_dict['Instagram']+query
		response = requests.get(request_url)
		data = response.json()
		return data['graphql']['user']['edge_followed_by']['count']

	def get_data(self):

		yt = self.get_youtube_subscribers()
		tw = self.get_twitter_subscribers()
		insta = self.get_intagram_subscribers()
		data ={
			'YouTube': yt,
			'Twitter': tw,
			'Instagram': insta 
		}
		return data

	def display_data(self, data=None):

		if data == None:
			print('need to data to display...')
			return None

		image = Image.new('1', (self.oled.width, self.oled.height))
		draw = ImageDraw.Draw(image)		
		x = 0
		top = -2
		spacing_increment = 15
		youtube_sub = 'pwdie Yt: '+str(data['YouTube'])
		twitter_sub = 'RDJ Twtr: '+str(data['Twitter'])
		instagram_sub = 'nasa Insta: '+str(data['Instagram'])

		draw.text((x,top), youtube_sub, font=self.font, fill=255)
		draw.text((x, top+spacing_increment), twitter_sub, font=self.font, fill=255)
		spacing = spacing_increment*2
		draw.text((x, top+spacing), instagram_sub, font=self.font, fill=255)
		print('showing image')
		self.oled.image(image)
		self.oled.show()

	def display_images(self):
		oled.fill(0)
		oled.show()
		for image in self.images:
			image = Image.open(image).resize((oled.width, oled.height), Image.ANTIALIAS).convert('1')
			draw = ImageDraw.Draw(image)
			oled.image(image)
			oled.show()
			time.sleep(0.5)

	def display_LED(self):
		pixels = neopixel.NeoPixel(board.D18, 8)
		for i in range(8):
			pixels[i] = (0,255,255)


if __name__ == '__main__':
	account_dict = {'YouTube':'PewDiePie',
					'Twitter':'RobertDowneyJr',
					'Instagram':'nasa'}

	images = []
	credentials_dict = {}
	'''
	open credentials_file.txt with comma separation
	Ex.
		YouTube,API_CREDENTIALS
		Twitter,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_SECRET
	'''
	'''
	with open("credentials.txt", "r") as file:
		for line in file:
			#split on first comma
			information = line.split(',',1)
			credentials_dict[information[0]] = tuple(information[1].split(','))

	'''
	credentials_dict={'YouTube':'AIzaSyAGMq4k-PIhEsocN40SBovIk3TK8-USIMk',
			'Twitter':('Q75S5L18cSE19kMy3ouyQ7RcM','vS2kvcKUeo61Xo0w85tVwlb9nAW14G603mqAdRDyxJ0qPhjhRS',
				'1183051881200775168-0KPXoGfP8bfFdnlwZSRbMAfFGmQ6g0','NHfoIUYg94yjOpmlm82zDmxTVZjnWt4rb4JSo0pgJDDgC')}
	#print(credentials_dict)
	pi_sub = SubCount(account_dict, credentials_dict, images)

	data = pi_sub.get_data()
	pi_sub.display_data(data)
	#pi_sub.display_images(images)
	pi_sub.display_LED()

























