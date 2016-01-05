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
from kivy.network.urlrequest import UrlRequest
import subprocess
import json



# ***** Functions *********
MBurl='http://my.meteoblue.com/dataApi/dispatch.pl?apikey=41f2dd49fb6a&mac=feed&type=json_7day_3h_firstday&lat=43.5&lon=1.4133&asl=150&tz=Europe%2FZurich&city=Toulouse'

def toggle_radio(state,channel):
	print('toggle radio ' + str(state) + ' ' + str(channel))
	if state =='normal':
		#subprocess.check_output(["mpc","stop"])
		print('extinction radio')
	else:
		#subprocess.check_output(["mpc","play",str(channel)])
		print('allumage canal: ' + str(channel))

def get_weather(req, results):
	CurrentTemp = json.dumps(results['current']['temperature'])
	print('T Curr:',json.dumps(results['current']['temperature']))
	CurrentTemp = json.dumps(results['current']['temperature'])
	print('T Curr:',json.dumps(results['current']['temperature']))
	ForecastMaxTemp = json.dumps(results['forecast'][0]['temperature_max'])
	print('T Max:',json.dumps(results['forecast'][0]['temperature_max'], sort_keys=True, indent=4))
	ForecastMinTemp = json.dumps(results['forecast'][0]['temperature_min'])
	print('T Min:',json.dumps(results['forecast'][0]['temperature_min'], sort_keys=True, indent=4))
	Picto = int(json.dumps(results['current']['pictocode']))
	print('Picto: ',Picto)


# ***** Classes *******

class MainLayout(BoxLayout):
	pass

class KivyWeatherApp(App):
	source = StringProperty()
	UrlRequest(MBurl,on_success=get_weather)
	def build(self):
		mainlayout = MainLayout()
		inspector.create_inspector(Window, mainlayout)
		return mainlayout

if __name__ == "__main__":
	KivyWeatherApp().run()