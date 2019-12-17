#for data
import requests
from twython import Twython
#from youtube_api import YouTubeDataAPI

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
        print("Creating class object...")
        self.pixels = neopixel.NeoPixel(board.D18, 8)
        self.IMAGE_DIMENSIONS = (128, 64) #(width, height)
        self.R = 3
        self.G = 252
        self.B = 80
        self.account_dict = account_dict
        self.image_folder = "/home/pi/Desktop/RPi-Projects/images/oled_images/"
        self.images_list = images

        if font_file_path=='default':
            print("Font set: Default...")
            self.font = ImageFont.load_default()            
        else:
            #prints the filename from the filepath string, [-1]
            #the last element in the list
            print("Font set: ",font_file_path.split('/')[-1])
            self.font = ImageFont.truetype("arial.tff",15)
        
        #trying social medial credentials
        print("Activating Twitter API")
        self.twAPI_KEY, self.twAPI_SECRET, self.twACCESS_TOKEN, self.twACCESS_SECRET = credentials_dict['Twitter']
        self.twitter = Twython(self.twAPI_KEY, self.twAPI_SECRET,self.twACCESS_TOKEN, self.twACCESS_SECRET)

        #use I2C pin setup
        i2c = board.I2C()
        #define reset pin
        oled_reset = digitalio.DigitalInOut(board.D4)
        #create oled to display text/imgages
        self.oled = adafruit_ssd1306.SSD1306_I2C(self.IMAGE_DIMENSIONS[0], self.IMAGE_DIMENSIONS[1], i2c, addr=0x3c, reset=oled_reset)

    def get_twitter_subscribers(self, account=None):
        '''
        Get account data from twitter
        @param: account_dict - default None (uses currently stored information)
        @return: twitter sub data
        '''
        response = self.twitter.show_user(screen_name=self.account_dict['Twitter'])
        return response["followers_count"]

    def get_youtube_subscribers(self, account=None):
        channel_id = self.youtube.get_channel_id_from_user(self.account_dict['YouTube'])
        channel_data = self.youtube.get_channel_metadata(channel_id)
        return channel_data['subscription_count']

    def get_intagram_subscribers(self, account=None):
        '''
        This function gets data from instagram through
        the server they have running
        '''
        #we specify a domain url to go to
        url = "https://www.instagram.com/"

        #we then tell the server what we want. This is called a "query"
        query = "/?__a=1"

        #this is the request we will send to our function
        #self.account_dict['Instagram'] contains the channel we are asking
        #information about.
        request_url = url+self.account_dict['Instagram']+query
        response = requests.get(request_url)

        #json is a file format that is exactly the same as
        #python dictionaries so we can navigate through
        #the file to get the information we want
        data = response.json()
        return data['graphql']['user']['edge_followed_by']['count']

    def get_data(self):

        #yt = self.get_youtube_subscribers()
        tw = self.get_twitter_subscribers()
        yt = "None"
        insta = self.get_intagram_subscribers()
        data ={
            'YouTube': yt,
            'Twitter': tw,
            'Instagram': insta 
        }
        return data

    def display_data(self, data):
        '''
        This function displays your data, for example,
        subscriber count you got from a channel.

        Things you need to give your function:
        the only thing you need is data which is a dictionary   
        '''
        #line below makes a new image the size of the OLED screen to display
        #think of this like a canvas, we will "paint" text over this below
        image = Image.new('1', (self.oled.width, self.oled.height))

        #line below makes an object of class Draw that will let us draw on the
        #image we created in the line above 
        draw = ImageDraw.Draw(image)    

        #below we make strings to print as text. make sure everything you add
        #with the plus sign (+) is a string.
        youtube_sub = 'pwdie Yt: '+str(data['YouTube'])
        twitter_sub = 'RDJ Twtr: '+str(data['Twitter'])
        instagram_sub = 'nasa Insta: '+str(data['Instagram'])

        #x is how far left or right you want to start your text 
        x = 0
        
        #top is how far up you want to start your text, 0 is the TOP of the
        #screen so -2 brings it DOWN 2 pixels.
        top = -2

        #we are calling a function that is in a class with the dot "." to draw text
        #the first thing we give this function is a tuple of where we
        #want to start, like a coordinate. the next thing we give is the string we
        #made before this, we then give it the font, and then we specify to fill all
        #the Red, Green, Blue values to the max (255) to give us white.
        draw.text((x,top), youtube_sub, font=self.font, fill=255)
        
        #this is how much spacing we want between our text
        spacing_increment = 20

        #we use the function again to place a second string of text except now we
        #use our spacing
        draw.text((x, top+spacing_increment), twitter_sub, font=self.font, fill=255)
        
        #we redo our spacing for the next text, making it a little bigger or else
        # it will overlap what we told it to write
        spacing = spacing_increment*2
        
        #Finally we write our last text just as we did before
        draw.text((x, top+spacing), instagram_sub, font=self.font, fill=255)
        
        #this is for us to know when it will show the text      
        print('showing text...')

        #now we actually show it by calling the function 'image' and giving it
        #the image we drew text on
        self.oled.image(image)

        #finally we tell the screen to show what we created
        self.oled.show()

    def display_images(self):
        '''
        This function displays images on the OLED screen.
        '''
        #clear the screen by setting all the color
        #values to 0
        self.oled.fill(0)
        
        #show that it is clear
        self.oled.show()

        #for loop to go through the image files we specified in a list
        for image in self.images_list:
            #open the image, resize it to fit the screen, convert to one color
            print("Displaying: ",image)
            image_name = self.image_folder+image
            image_name = Image.open(image_name).resize((self.oled.width, self.oled.height), Image.ANTIALIAS).convert('1')
    
            #draw the image on the screen           
            draw = ImageDraw.Draw(image_name)
            self.oled.image(image_name)
            self.oled.show()

            #wait 0.5 seconds until we can show the next image
            time.sleep(0.5)

    def display_LED(self):
        print("showing LED sequence...")
        
        self.pixels.fill((0,0,0))
        direction = 1 #direction is for moving towards pink or away
        start = 0
        end = 3
        for i in range(4):
            for _ in range(43):
                for i in range(start,end):
                    self.pixels[i] = (self.R,self.G,self.B)
                time.sleep(0.1)
                self.B += direction*4
            for _ in range(61):
                for i in range(start,end):
                    self.pixels[i]=(self.R,self.G,self.B)
                time.sleep(0.1)
                self.G += -1*direction*4
            for _ in range(61):
                for i in range(start,end):
                    self.pixels[i] = (self.R,self.G,self.B)
                time.sleep(0.1)
                self.R += direction*4
            direction *= -1 #changes the direction to go the other way
            print('direction: ',direction)
            for i in range(start, end):
                self.pixels[i] = ((0,0,0))
            start += -1*direction*4
            end += -1*direction*4


if __name__ == '__main__':
    account_dict = {'YouTube':'PewDiePie',
                    'Twitter':'RobertDowneyJr',
                    'Instagram':'nasa'}

    #list of images to display, make sure they are all in the same folder
    #"images/oled_images"
    images = ["siliconSTEM.jpeg","ironman.jpeg","hulk.jpg"]

    #these are the keys to the API being used
    credentials_dict={'YouTube':'AIzaSyAGMq4k-PIhEsocN40SBovIk3TK8-USIMk',
            'Twitter':('Q75S5L18cSE19kMy3ouyQ7RcM','vS2kvcKUeo61Xo0w85tVwlb9nAW14G603mqAdRDyxJ0qPhjhRS',
                '1183051881200775168-0KPXoGfP8bfFdnlwZSRbMAfFGmQ6g0','NHfoIUYg94yjOpmlm82zDmxTVZjnWt4rb4JSo0pgJDDgC')}
    #print(credentials_dict)
    pi_sub = SubCount(account_dict, credentials_dict, images)
    while(True):
        pi_sub.display_images()
        data = pi_sub.get_data()
        pi_sub.display_data(data)
        pi_sub.display_LED()

























