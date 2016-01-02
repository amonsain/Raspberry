import json
import webbrowser
#import urllib.request --- only for Python3
import urllib
from sense_hat import SenseHat
import time
from time import gmtime, strftime, localtime
import string
import math

#Weather API URL, returns a JSON data scheme. Set your own API key and Location
url='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'
update_period = 30		 #update period @which the weather API is called to update data (minutes)

AltitudeAboveSeaLevel = 150
BaroCompensation = 4

ShowTime = True
ShowTemperature = True
ShowWeatherPicto = True
ShowHumidity = False
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



def main():

	sense = SenseHat()
	sense.low_light = True
	last_update_time = 0
	sense.rotation = 90

	SunPictos = [1,2,3,4,5,6,13,14,15]
	SunCloudPictos = [7,8,9,10,11,12,31,32]
	CloudPictos = [16,17,18,19,20,21,22,23]
	RainPictos = [23,25,33,35]
	SnowPictos = [24,26,29,34]
	StormPictos = [27,28,30]

	while True:  

		# Fetch weather data every update period
		if time.time()-last_update_time > update_period*60:
			Weather = get_weather(url)
			last_update_time = time.time()
			Baro = get_press(AltitudeAboveSeaLevel)
			Humidity = sense.get_humidity()
			print('Current, Max, Min temp, Picto:',Weather.CurrentTemp,Weather.ForecastMaxTemp,Weather.ForecastMinTemp,Weather.Picto)
			print('Weather info updated at:', strftime("%a, %d %b %Y %H:%M:%S", localtime()))
			print('Local Pressure',Baro)


 
		# display Time & Weather info on SenseHat

		if ShowTime:
			sense.show_message('{} {}'.format('Heure:',strftime("%H:%M",localtime())),text_colour=(180,180,180))

		if ShowTemperature:
			sense.show_message('{} {}{}'.format('T:', str(Weather.CurrentTemp),' '), text_colour=Weather.CurrentColor,scroll_speed=0.15)
			sense.show_message('{} {}'.format('Max:', str(Weather.ForecastMaxTemp)), text_colour=Weather.MaxColor,scroll_speed=0.15)
			sense.show_message('{} {}'.format('Min:', str(Weather.ForecastMinTemp)), text_colour=Weather.MinColor,scroll_speed=0.15)

		if ShowWeatherPicto:

			if Weather.Picto in SunPictos:
				for i in range (0,10):
					sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/soleil.png")
					time.sleep(0.3)
					sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/soleil2.png")
					time.sleep(0.3)
			elif Weather.Picto in SunCloudPictos:
				sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/soleil&nuage.png")
				time.sleep(5)
			elif Weather.Picto in CloudPictos:
				sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/nuage.png")
				time.sleep(5)
			elif Weather.Picto in RainPictos:
				sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/nuage&pluie.png")
				time.sleep(5)
			elif Weather.Picto in SnowPictos:
				sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/nuage&neige.png")
				time.sleep(5)
			elif Weather.Picto in StormPictos:
				sense.load_image("/home/pi/SenseHat/WeatherMonitor/Images/nuages&eclairs.png")
				time.sleep(5)												
		
		if ShowPressure:
			sense.show_message('{} {}'.format(format(Baro, '.1f'),'hPa'), text_colour=Weather.CurrentColor,scroll_speed=0.15)
			#print(format(Baro, '.1f'),'hPa')

		if ShowHumidity:
			sense.show_message('{} {} {}'.format(format(Humidity, '.1f'),'%','Hum.'), text_colour=Weather.CurrentColor,scroll_speed=0.15)
			#print(format(Humidity, '.1f'),'%','Hum.')


		time.sleep(1)




if __name__=="__main__":
	main()	















