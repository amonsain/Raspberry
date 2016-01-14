from kivy.app import App
from kivy.core.window import Window
from kivy.modules import inspector
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition
from KivyRadio import *
from KivyWeather import *
from ClockButton import ClockButton
import locale

#locale.setlocale(locale.LC_ALL, 'fr_FR')

class MyScreenManager(ScreenManager):
    pass

class RadioScreen(Screen):
	pass

class WeatherScreen(Screen):
	pass


####### MAIN

class KivyHomeScreenApp(App):
	#source = StringProperty()

	def build(self):
		mainlayout = MyScreenManager()
		init_radio()
		mainlayout.add_widget(RadioScreen(name='Radio'))
		mainlayout.add_widget(WeatherScreen(name='Weather'))
		inspector.create_inspector(Window, mainlayout)
		return mainlayout

if __name__ == "__main__":
	KivyHomeScreenApp().run()