from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.modules import inspector
from kivy.clock import Clock
import time
import urllib
import subprocess
import json
import datetime

# Clock Example for data update http://stackoverflow.com/questions/18923321/making-a-clock-in-kivy
# ***** Functions *********
MBurl='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'


def get_daily_weather(url):
# Get weather info from MeteoBlue's API
# Fetch URL, parse & return a list of DaylyData objects
 
  #retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3
	#retour_api_meteo = urllib.urlopen(url)
	#Json_string = retour_api_meteo.read().decode('utf-8')
	#Json_decoded = json.loads(Json_string)
# Get Weather data from Json structure
	daylyforecastlist = []
	#for i in range(0,len(Json_decoded['forecast'])):
	for i in range(0,4):
		ForecastMaxTemp = 'A'
		ForecastMinTemp = 'B'
		Picto = 'C'
		# ForecastMaxTemp = json.dumps(Json_decoded['forecast'][i]['temperature_max'])
		# ForecastMinTemp = json.dumps(Json_decoded['forecast'][i]['temperature_min'])
		# Picto = int(json.dumps(Json_decoded['forecast'][i]['pictocode_day']))
		updatetime = time = datetime.datetime.now()
		i = DailyData(updatetime,ForecastMaxTemp,ForecastMinTemp,Picto)
		daylyforecastlist.append(i)

	for i in range(0,4):
		print(daylyforecastlist[i].ForecastMaxTemp)
		print(daylyforecastlist[i].ForecastMinTemp)
		print(daylyforecastlist[i].Picto)
		print(daylyforecastlist[i].updatetime)

	return daylyforecastlist





# ***** Classes *******

class MainLayout(BoxLayout):
	pass

class DailyData(object):
  def __init__(self,updatetime,ForecastMaxTemp, ForecastMinTemp, Picto):
	self.ForecastMaxTemp = ForecastMaxTemp
	self.ForecastMinTemp = ForecastMinTemp
	self.Picto = Picto
	self.updatetime = updatetime


class Daytemp(Label):
    def __init__(self,index, **kwargs):
        super(Daytemp, self).__init__(**kwargs)
        self.bind(pos=self.updatetemp)
        self.bind(size=self.updatetemp)
        self.index=index


class KivyWeatherApp(App):
	DayWeatherList = ListProperty()
	DayWeatherList = get_daily_weather(MBurl)
	print('Hello picto' + str(DayWeatherList[1].Picto))

	def increase(*arg):
		print('updating')
		DayWeatherList = get_daily_weather(MBurl)
		#DayWeatherList[1].ForecastMaxTemp = DayWeatherList[1].ForecastMaxTemp +1
		return 'oj'

	def build(self):
		mainlayout = MainLayout()
		inspector.create_inspector(Window, mainlayout)
		Clock.schedule_interval(self.increase, 1)

		return mainlayout



	

if __name__ == "__main__":
	KivyWeatherApp().run()