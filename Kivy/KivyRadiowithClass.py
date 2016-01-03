from kivy.app import App

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
import subprocess


class MainLayout(BoxLayout):
	pass

class RadioButton(ToggleButton):
	icon = StringProperty(None)
	RadioBox = BoxLayout()
	def __init__(self,station='',*args,**kwargs):
		super(RadioButton,self).__init__(*args,**kwargs)
		self.station = station
		self.icon = 'playbuttonwhite.png'
		self.group='Station'
	def on_press(self):
		print('press Station ' + str(self.station))
		if self.state == 'normal':
			self.icon = 'playbuttonwhite.png'
		else: self.icon = 'whitepause.png'
		print(str(self.icon))



class KivyRadioClassApp(App):
	source = StringProperty()
	def build(self):
		self.playing = False
		return MainLayout()

	def toggle_radio(self,state,channel):
		print('toggle radio ' + str(state) + ' ' + str(channel))
		if state =='normal':
			subprocess.check_output(["mpc","stop"])
			self.playing = False
			print('extinction radio')
		else:
			subprocess.check_output(["mpc","play",str(channel)])
			self.playing = True
			print('allumage canal: ' + str(channel))

	def change_volume(self,level):
		print('Change volume' + str(level))
		subprocess.check_output(["mpc","volume",str(level)])



if __name__ == "__main__":
	KivyRadioClassApp().run()