from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition
from KivyRadiowithClass import *
from KivyWeather import *


class MyScreenManager(ScreenManager):
    pass

class RadioScreen(Screen):
	pass

class WeatherScreen(Screen):
	pass


####### MAIN

class KivyRadioScreenApp(App):
	#source = StringProperty()

	def build(self):
		mainlayout = MyScreenManager()
		init_radio()
		mainlayout.add_widget(RadioScreen(name='Radio'))
		mainlayout.add_widget(WeatherScreen(name='Weather'))
		inspector.create_inspector(Window, mainlayout)
		return mainlayout

if __name__ == "__main__":
	KivyRadioScreenApp().run()