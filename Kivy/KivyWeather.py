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

from time import gmtime, strftime, localtime
import urllib
import subprocess
import json
import datetime
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR')

# Clock Example for data update http://stackoverflow.com/questions/18923321/making-a-clock-in-kivy
# http://stackoverflow.com/questions/27213545/update-properties-of-a-kivy-widget-while-running-code
# ***** Functions *********
MBurl='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'



def get_daily_weather(url):
# Get daily weather info from MeteoBlue's API (all available upcoming days)
# Fetch URL, parse & return a list of DaylyData objects

  #retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3

	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)

# Get Weather data from Json structure
	updatetime = time = datetime.datetime.now()
	daylyforecastlist = []
	for i in range(0,4):
		Date = str(json.dumps(Json_decoded['forecast'][i]['date']))
		ForecastMaxTemp = json.dumps(Json_decoded['forecast'][i]['temperature_max'])
		ForecastMinTemp = json.dumps(Json_decoded['forecast'][i]['temperature_min'])
		MaxTempColor = hex_to_rgb(json.dumps(Json_decoded['forecast'][i]['temperature_max_color']))
		MinTempColor = hex_to_rgb(json.dumps(Json_decoded['forecast'][i]['temperature_min_color']))
		WindSpeed = json.dumps(Json_decoded['forecast'][i]['wind_speed_max'])
		WindDir = json.dumps(Json_decoded['forecast'][i]['wind_direction_dominant'])
		WinMax = json.dumps(Json_decoded['forecast'][i]['wind_gust_max'])
		Uv = json.dumps(Json_decoded['forecast'][i]['uv_index'])
		UvColor = hex_to_rgb(json.dumps(Json_decoded['forecast'][i]['uv_color']))
		RainProb = json.dumps(Json_decoded['forecast'][i]['precipitation_probability'])
		RainMm = json.dumps(Json_decoded['forecast'][i]['precipitation_amount'])
		Picto = int(json.dumps(Json_decoded['forecast'][i]['pictocode_day']))
		i = DailyData(Date,ForecastMaxTemp,MaxTempColor,ForecastMinTemp,MinTempColor,WindSpeed,WindDir,WinMax,Uv,UvColor,RainProb,RainMm,Picto)
		daylyforecastlist.append(i)

	return daylyforecastlist


def get_current_weather(url):
# Get current weather info from MeteoBlue's API
# Fetch URL, parse & return a list of DaylyData objects

  #retour_api_meteo = urllib.request.urlopen(url)  --- only for Python3

	retour_api_meteo = urllib.urlopen(url)
	Json_string = retour_api_meteo.read().decode('utf-8')
	Json_decoded = json.loads(Json_string)

# Get Weather data from Json structure
	updatetime = 'Mise a jour: '+ strftime("%d %b %H:%M", localtime())
	CurrentTemp = json.dumps(Json_decoded['current']['temperature'])
	Picto = int(json.dumps(Json_decoded['current']['pictocode']))
	Sunrise = json.dumps(Json_decoded['forecast'][0]['sunrise_time'])
	Sunset = json.dumps(Json_decoded['forecast'][0]['sunset_time'])
	Pressure = json.dumps(Json_decoded['forecast'][0]['pressure_hpa'])
	IsDaylight =  json.dumps(Json_decoded['current']['is_daylight'])
	currentweather = CurrentData(updatetime,CurrentTemp,Sunrise,Sunset,Pressure,IsDaylight, Picto)

	return currentweather




def get_weathericon(id):
	if id < 10:
		iconname = './pictogramssvg/'+'0'+str(id)+'_day.svg.png'
	else: iconname = './pictogramssvg/'+str(id)+'_day.svg.png'
	return iconname


def hex_to_rgb(value):
  value = value.lstrip('"#')
  value = value.rstrip('"')
  #print(value)
  lv = len(value)
  #print(lv)
  return tuple(int(value[i:int(i+lv/3)], 16) for i in range(0, lv, int(lv/3)))

#***** Classes *******


class MainLayout(BoxLayout):
	pass


#****** Current wather + moon/UV Sunset info about today

class WeatherCurrent(BoxLayout):
	dayweatherlist = ListProperty(None)

	def __init__(self,currentweather='',*args,**kwargs):
		super(WeatherCurrent,self).__init__(*args,**kwargs)
		print('create WeatherCurrent')
		self.textcolor=[0.2,0.5,0.9,1]
		self.currentweather = currentweather
		Clock.schedule_once(self.update, 0.5)
		Clock.schedule_interval(self.update, 1800)
		# could create widgets from here, label them with an id: and update them in the following class method self.ids.idname = ...
 	def update(self, *args):
		self.currentweather = get_current_weather(MBurl)
 		self.clear_widgets()
 		self.add_widget(Label(text='Current Temp: '+ str(self.currentweather.CurrentTemp),color=self.textcolor))
 		self.add_widget(Label(text=str(self.currentweather.updatetime),color=self.textcolor))
 		self.add_widget(Image(source=get_weathericon(self.currentweather.Picto)))


class WeatherDay(BoxLayout):
	dayweatherlist = ListProperty(None)
	def __init__(self,dayweatherlist='',dayid='',*args,**kwargs):
		super(WeatherDay,self).__init__(*args,**kwargs)
		print('create WeatherDay')
		self.textcolor=[0.2,0.5,0.9,1]
		self.dayweatherlist = dayweatherlist
		Clock.schedule_once(self.update, 0.5)
		Clock.schedule_interval(self.update, 7200)
		# could create widgets from here, label them with an id: and update them in the following class method self.ids.idname = ...
 	def update(self, *args):
 		self.dayweatherlist = get_daily_weather(MBurl)
 		self.clear_widgets()
 		self.add_widget(Label(text='Jour' +str(self.dayweatherlist[self.dayid].Date),color=self.textcolor))
 		self.add_widget(Image(source=get_weathericon(self.dayweatherlist[self.dayid].Picto)))
 		self.add_widget(Label(text='Maxi: '+ str(self.dayweatherlist[self.dayid].ForecastMaxTemp),color=self.textcolor))
 		self.add_widget(Label(text='Mini: '+ str(self.dayweatherlist[self.dayid].ForecastMinTemp),color=self.textcolor))





class DailyData(object):
  def __init__(self,Date, ForecastMaxTemp,MaxTempColor,ForecastMinTemp,MinTempColor,WindSpeed,WindDir,WindMax,Uv, UvColor,RainProb,RainMm,Picto):
	self.Date = Date
	self.ForecastMaxTemp = ForecastMaxTemp
	self.MaxTempColor = MaxTempColor
	self.ForecastMinTemp = ForecastMinTemp
	self.MinTempColor = MinTempColor
	self.WindSpeed = WindSpeed
	self.WindDir = WindDir
	self.WindMax = WindMax
	self.Uv = Uv
	self.UvColor = UvColor
	self.RainProb = RainProb
	self.RainMm = RainMm
	self.Picto = Picto


class CurrentData(object):
  def __init__(self,updatetime,CurrentTemp,Sunrise,Sunset,Pressure,IsDaylight, Picto):
	self.updatetime = updatetime
	self.CurrentTemp = CurrentTemp
	self.Picto = Picto
	self.Sunrise = Sunrise
	self.Sunset = Sunset
	self.Pressure = Pressure
	self.IsDaylight = IsDaylight


class KivyWeatherApp(App):

	def build(self):
		print('Program start at:', strftime("%a, %d %b %Y %H:%M:%S", localtime()))
		Window.clearcolor = (0.95, 0.95, 0.95, 1)
		self.mainlayout = MainLayout()
		inspector.create_inspector(Window, self.mainlayout)
		return self.mainlayout



if __name__ == "__main__":
	KivyWeatherApp().run()
