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
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition
from kivy.clock import Clock
import time
import urllib
import subprocess
import json
import datetime




# ***** Functions Radio *********

def toggle_radio(state,channel):
	print('toggle radio ' + str(state) + ' ' + str(channel))
	if state =='normal':
		#subprocess.check_output(["mpc","stop"])
		print('extinction radio')
	else:
		#subprocess.check_output(["mpc","play",str(channel)])
		print('allumage canal: ' + str(channel))

def change_volume(level):
	print('Change volume' + str(level))
	#subprocess.check_output(["mpc","volume",str(level)])


def init_radio():
	pass


# ***** Functions Weather *********
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





class MyScreenManager(ScreenManager):
    pass

# ***** Classes Radio *******



class RadioScreen(Screen):
	pass

class VolumeSlider(Slider):
	def __init__(self,*args,**kwargs):
		super(VolumeSlider,self).__init__(*args,**kwargs)
		self.value=25
		print(self.value)
		self.bind(value=self.update_value)

	def update_value(self,*args):
		change_volume(int(self.value))


class RadioButton(ToggleButton):
	#icon = StringProperty(None)
	def __init__(self,stationid='',stationname='',*args,**kwargs):
		super(RadioButton,self).__init__(*args,**kwargs)
		self.stationid = stationid
		self.stationname = stationname
		self.group='Station'



		with self.canvas.after:
			self.radiobox = BoxLayout(orientation='horizontal')
			self.radiobuttonlabel = Label(font_size=40,size_hint=[0.8,1])
			self.radiobuttonimage = Image(source='./images/playbuttonwhite.png',size_hint=[0.2,1])			
			self.radiobox.add_widget(self.radiobuttonlabel)
			self.radiobox.add_widget(self.radiobuttonimage)	
			self.add_widget(self.radiobox)
			self.background_normal = ''
			self.background_down = ''
			self.background_color = [1,1,1,1]

		self.bind(pos=self.update_radiobox,size=self.update_radiobox)
		self.bind(state=self.update_state)

	def update_radiobox(self,*args):
		self.radiobox.pos = self.pos
		self.radiobox.size = self.size
		self.radiobuttonlabel.text = str(self.stationname)


	def update_state(self,*args):
		print('update state')
		if self.state == 'normal':
			self.radiobuttonimage.source = './images/playbuttonwhite.png'
		else: self.radiobuttonimage.source  = './images/whitepause.png'

	def on_press(self):
		print('press Station ' + str(self.stationid))
		toggle_radio(self.state,self.stationid)



###### classes Weather

class WeatherScreen(Screen):
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



####### MAIN

class KivyRadioScreenApp(App):
	source = StringProperty()
	def build(self):
		mainlayout = MyScreenManager()
		init_radio()
		mainlayout.add_widget(RadioScreen(name='Radio'))
		mainlayout.add_widget(WeatherScreen(name='Weather'))
		inspector.create_inspector(Window, mainlayout)
		return mainlayout

if __name__ == "__main__":
	KivyRadioScreenApp().run()