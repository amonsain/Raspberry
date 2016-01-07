from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
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
# http://stackoverflow.com/questions/27213545/update-properties-of-a-kivy-widget-while-running-code
# ***** Functions *********
MBurl='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'



def get_daily_weather_stub(url):


# Get Weather Fake
	updatetime = time = datetime.datetime.now()
	daylyforecastlist = []
	for i in range(0,5):
		ForecastMaxTemp = 'A'+str(i)
		ForecastMinTemp = 'B'+str(i)
		Picto = i
		Date = str(i)
		i = DailyData(str(updatetime),Date,ForecastMaxTemp,ForecastMinTemp,Picto)
		daylyforecastlist.append(i)

	return daylyforecastlist




def get_daily_weather(url):
# Get weather info from MeteoBlue's API
# Fetch URL, parse & return a list of DaylyData objects

  #retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3

	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)

# Get Weather data from Json structure
	updatetime = time = datetime.datetime.now()
	daylyforecastlist = []
	for i in range(0,len(Json_decoded['forecast'])):
		ForecastMaxTemp = json.dumps(Json_decoded['forecast'][i]['temperature_max'])
		ForecastMinTemp = json.dumps(Json_decoded['forecast'][i]['temperature_min'])
		Picto = int(json.dumps(Json_decoded['forecast'][i]['pictocode_day']))
		Date = str(json.dumps(Json_decoded['forecast'][i]['date']))
		i = DailyData(str(updatetime),Date,ForecastMaxTemp,ForecastMinTemp,Picto)
		daylyforecastlist.append(i)

	return daylyforecastlist


def get_weathericon(id):
	if id < 10:
		iconname = './pictogramssvg/'+'0'+str(id)+'_day.svg.png'
	else: iconname = './pictogramssvg/'+str(id)+'_day.svg.png'
	return iconname


#***** Classes *******

class MainLayout(BoxLayout):
	pass


class WeatherDay(BoxLayout):
	dayweatherlist = ListProperty(None)
	def __init__(self,dayweatherlist='',dayid='',*args,**kwargs):
		super(WeatherDay,self).__init__(*args,**kwargs)
		print('create WeatherDay')
		self.dayweatherlist = dayweatherlist
		Clock.schedule_once(self.update_dayweather, 0.5)
		Clock.schedule_interval(self.update_dayweather, 600)
		# could create widgets from here, label them with an id: and update them in the following class method self.ids.idname = ...
 	def update_dayweather(self, *args):
 		self.dayweatherlist = get_daily_weather(MBurl)
 		self.clear_widgets()
 		self.add_widget(Label(text= str(self.dayweatherlist[self.dayid].Date)))
 		self.add_widget(Label(text='Temp Max: '+ str(self.dayweatherlist[self.dayid].ForecastMaxTemp)))
 		self.add_widget(Label(text='Temp Min: '+ str(self.dayweatherlist[self.dayid].ForecastMinTemp)))
 		self.add_widget(Image(source=get_weathericon(self.dayweatherlist[self.dayid].Picto)))
 		self.add_widget(Label(text=str(self.dayweatherlist[self.dayid].updatetime)))


class DailyData(object):
  def __init__(self,updatetime,Date, ForecastMaxTemp, ForecastMinTemp, Picto):
	self.Date = Date
	self.ForecastMaxTemp = ForecastMaxTemp
	self.ForecastMinTemp = ForecastMinTemp
	self.Picto = Picto
	self.updatetime = updatetime


class KivyWeatherApp(App):

	def build(self):
		Window.clearcolor = (0.2, 0.2, 0.2, 1)
		self.mainlayout = MainLayout()
		inspector.create_inspector(Window, self.mainlayout)
		return self.mainlayout



if __name__ == "__main__":
	KivyWeatherApp().run()
