from __future__ import print_function
import json
import webbrowser
#import urllib.request --- only for Python3
import urllib
from sense_hat import SenseHat
import time
import datetime
import dateutil.parser
from time import gmtime, strftime, localtime
import string
import math
import httplib2
import os


### imports for Google Calendar API
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
try:
		import argparse
		flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
		flags = None


# Google Calendar API Authentication Functions

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret_136349925937-1mfpj0jrr3gurh45v6gfm5mp6djbi982.apps.googleusercontent.com.json'
APPLICATION_NAME = 'CalendrierMaison'


def get_credentials():
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
				Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
				os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
																	 'calendar-python-quickstart.json')

		store = oauth2client.file.Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
				flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
				flow.user_agent = APPLICATION_NAME
				if flags:
						credentials = tools.run_flow(flow, store, flags)
				else: # Needed only for compatibility with Python 2.6
						credentials = tools.run(flow, store)
				print('Storing credentials to ' + credential_path)
		return credentials



# Weather related functions
#Weather API URL, returns a JSON data scheme. Set your own API key and Location
url='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'
update_period = 30     #update period @which the weather API is called to update data (minutes)

AltitudeAboveSeaLevel = 150
BaroCompensation = 4

ShowTime = True
ShowTemperature = True
ShowWeatherPicto = True
ShowHumidity = True
ShowPressure = True



class WeatherData(object):
	def __init__(self, CurrentTemp, ForecastMaxTemp, ForecastMinTemp, CurrentColor, MaxColor, MinColor,Picto):
		self.CurrentTemp = CurrentTemp
		self.ForecastMaxTemp = ForecastMaxTemp
		self.ForecastMinTemp = ForecastMinTemp
		self.CurrentColor = CurrentColor
		self.MaxColor = MaxColor
		self.MinColor = MinColor
		self.Picto = Picto

def hex_to_rgb(value):
	value = value.lstrip('"#')
	value = value.rstrip('"')
	#print(value)
	lv = len(value)
	#print(lv)
	return tuple(int(value[i:int(i+lv/3)], 16) for i in range(0, lv, int(lv/3)))



def get_weather(url):
# Get weather info from MeteoBlue's API
# Fetch URL, format data as string and decode as Json structure
	
	#retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3
	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)
	

# Get Weather data from Json structure

	CurrentTemp = json.dumps(Json_decoded['current']['temperature'])
	#print('T Curr:',json.dumps(Json_decoded['current']['temperature']))

	ForecastMaxTemp = json.dumps(Json_decoded['forecast'][0]['temperature_max'])
	#print('T Max:',json.dumps(Json_decoded['forecast'][0]['temperature_max'], sort_keys=True, indent=4))

	ForecastMinTemp = json.dumps(Json_decoded['forecast'][0]['temperature_min'])
	#print('T Min:',json.dumps(Json_decoded['forecast'][0]['temperature_min'], sort_keys=True, indent=4))

	CurrentColor = hex_to_rgb(json.dumps(Json_decoded['current']['temperature_color']))
	#print('CurrColor:', CurrentColor)

	MaxColor = hex_to_rgb(json.dumps(Json_decoded['forecast'][0]['temperature_max_color']))

	MinColor = hex_to_rgb(json.dumps(Json_decoded['forecast'][0]['temperature_min_color']))

	Picto = int(json.dumps(Json_decoded['current']['pictocode']))

	return WeatherData(CurrentTemp, ForecastMaxTemp, ForecastMinTemp,CurrentColor, MaxColor, MinColor,Picto)

# get Pressure
# returns the Pressure as a float, compensated to sea level
def get_press(altitude):

	compensation = 4

 # enable SenseHat modules
	from sense_hat import SenseHat
	
	sense=SenseHat()
	raw_pressure1 = sense.get_pressure()
	time.sleep(0.1) 
	raw_pressure2 = sense.get_pressure()
	time.sleep(0.1) 
	raw_pressure3 = sense.get_pressure()
	raw_pressure=(raw_pressure1+raw_pressure2+raw_pressure3)/3
	if raw_pressure != 0 :
		pressure = raw_pressure/math.pow(1 - 0.0065*altitude/288.15,5.25588)-compensation
		#print(pressure)
	return pressure





# Main Program

def main():

	#parameters
	last_update_time = 0



	#Initialize Sense Hat

	sense = SenseHat()
	sense.low_light = True
	sense.rotation = 90

	#Initialize Google Calendar

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)


		# Main Loop

	while True:  

		# Fetch weather & calendar data every update period
		if time.time()-last_update_time > update_period*60:
			Weather = get_weather(url)
			last_update_time = time.time()
			Baro = get_press(AltitudeAboveSeaLevel)
			Humidity = sense.get_humidity()
			print('Current, Max, Min temp:',Weather.CurrentTemp,Weather.ForecastMaxTemp,Weather.ForecastMinTemp)
			print('Weather info updated at:', strftime("%a, %d %b %Y %H:%M:%S", localtime()))
			print('Local Pressure',Baro)

			now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
			print('Getting the upcoming 10 events')
			eventsResult = service.events().list(
				calendarId='primary', timeMin='2011-06-03T10:00:00-07:00', maxResults=2, singleEvents=True,
				orderBy='startTime').execute()
			events = eventsResult.get('items', [])

			print(events)

			if not events:
				print('No upcoming events found.')
			for event in events:
				start = event['start'].get('dateTime', event['start'].get('date'))
				print(start, event['summary'])




		# Fetch Calendar data

		
 
		# display Weather info on SenseHat
		for event in events:
			eventtime=dateutil.parser.parse(event['start'].get('dateTime'))
			print(eventtime.strftime('%I:%M'))
			sense.show_message(eventtime.strftime('%I:%M'))
			sense.show_message(event['summary'])

		# if ShowTemperature:
		# 	sense.show_message('{} {}{}'.format('T:', str(Weather.CurrentTemp),' '), text_colour=Weather.CurrentColor,scroll_speed=0.15)
		# 	sense.show_message('{} {}'.format('Max:', str(Weather.ForecastMaxTemp)), text_colour=Weather.MaxColor,scroll_speed=0.15)
		# 	sense.show_message('{} {}'.format('Min:', str(Weather.ForecastMinTemp)), text_colour=Weather.MinColor,scroll_speed=0.15)
		
		# if ShowTime:
		# 	sense.show_message('{} {}'.format('Heure:',strftime("%H:%M",localtime())))

		# if ShowWeatherPicto:

		# 	if Weather.Picto > 0:
		# 		sense.load_image("Soleil.png")
		# 		time.sleep(3)
		
		# if ShowPressure:
		# 	sense.show_message('{} {}'.format(format(Baro, '.1f'),'hPa'), text_colour=Weather.CurrentColor,scroll_speed=0.15)
		# 	#print(format(Baro, '.1f'),'hPa')

		# if ShowHumidity:
		# 	sense.show_message('{} {} {}'.format(format(Humidity, '.1f'),'%','Hum.'), text_colour=Weather.CurrentColor,scroll_speed=0.15)
		# 	#print(format(Humidity, '.1f'),'%','Hum.')


		time.sleep(1)








if __name__=="__main__":
	main()  















