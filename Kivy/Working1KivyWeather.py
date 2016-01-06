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
# http://stackoverflow.com/questions/27213545/update-properties-of-a-kivy-widget-while-running-code
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
	updatetime = time = datetime.datetime.now()
	daylyforecastlist = []
	#for i in range(0,len(Json_decoded['forecast'])):
	for i in range(0,4):
		ForecastMaxTemp = 'A'+str(i)
		ForecastMinTemp = 'B'+str(i)
		Picto = 'C'+str(i)
		# ForecastMaxTemp = json.dumps(Json_decoded['forecast'][i]['temperature_max'])
		# ForecastMinTemp = json.dumps(Json_decoded['forecast'][i]['temperature_min'])
		# Picto = int(json.dumps(Json_decoded['forecast'][i]['pictocode_day']))
		i = DailyData(str(updatetime)+str(i),ForecastMaxTemp,ForecastMinTemp,Picto)
		daylyforecastlist.append(i)

	for i in range(0,4):
		print(daylyforecastlist[i].ForecastMaxTemp)
		print(daylyforecastlist[i].ForecastMinTemp)
		print(daylyforecastlist[i].Picto)
		print(daylyforecastlist[i].updatetime)

	return daylyforecastlist





#***** Classes *******

class MainLayout(BoxLayout):
	pass
		



class MainLayout2(BoxLayout):
	#dayweatherlist = ListProperty(None)
	def __init__(self,dayweatherlist=None,*args,**kwargs):
		print('creating Mainlayout2')
		super(MainLayout2,self).__init__(*args,**kwargs)
		self.dayweatherlist = dayweatherlist

 	def update_layout(self, *args):
 		self.dayweatherlist = get_daily_weather(MBurl)


class DailyData(object):
  def __init__(self,updatetime,ForecastMaxTemp, ForecastMinTemp, Picto):
	self.ForecastMaxTemp = ForecastMaxTemp
	self.ForecastMinTemp = ForecastMinTemp
	self.Picto = Picto
	self.updatetime = updatetime


class KivyWeatherApp(App):


# Standard sans self

	def build(self):
		dayweatherlist = get_daily_weather(MBurl)
		self.mainlayout = MainLayout()
		inspector.create_inspector(Window, self.mainlayout)
		Clock.schedule_interval(self.increase, 2)
		return self.mainlayout

	def increase(self,*arg):
		print('updating')
		dayweatherlist = get_daily_weather(MBurl)
		self.mainlayout.monlabel1H.text = str(dayweatherlist[0].updatetime)
		self.mainlayout.monlabel1P.text = str(dayweatherlist[0].Picto)
		self.mainlayout.monlabel2H.text = str(dayweatherlist[1].updatetime)
		self.mainlayout.monlabel2P.text = str(dayweatherlist[1].Picto)		


#Standard:
# 
# 	def build(self):
# 		self.dayweatherlist = get_daily_weather(MBurl)
# 		self.mainlayout = MainLayout()
# 		inspector.create_inspector(Window, self.mainlayout)
# 		Clock.schedule_interval(self.increase, 2)
# 		return self.mainlayout
# # 
# 	def increase(self,*arg):
# 		print('updating')
# 		self.dayweatherlist = get_daily_weather(MBurl)


# MainLayout2

	# def build(self):
	# 	DayWeatherList = get_daily_weather(MBurl)
	# 	print('weather received')
	# 	self.mainlayout = MainLayout2(DayWeatherList)
	# 	print(type(self.mainlayout))
	# 	#self.mainlayout = MainLayout()
	# 	print('main layout Build done')
	# 	print('one element in layout is :' + str(self.mainlayout.dayweatherlist[2].updatetime))
	# 	inspector.create_inspector(Window, self.mainlayout)
	# 	#Clock.schedule_interval(self.increase, 5)
	# 	return self.mainlayout





	

if __name__ == "__main__":
	KivyWeatherApp().run()