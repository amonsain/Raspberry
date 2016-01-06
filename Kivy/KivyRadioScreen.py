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
import subprocess



# ***** Functions *********

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

# ***** Classes *******

class MyScreenManager(ScreenManager):
    pass

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



class KivyRadioScreenApp(App):
	source = StringProperty()
	def build(self):
		mainlayout = MyScreenManager()
		init_radio()
		mainlayout.add_widget(RadioScreen(name='Radio1'))
		mainlayout.add_widget(RadioScreen(name='Radio2'))
		inspector.create_inspector(Window, mainlayout)
		return mainlayout

if __name__ == "__main__":
	KivyRadioScreenApp().run()