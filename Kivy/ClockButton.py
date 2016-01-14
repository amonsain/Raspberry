from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button

import datetime
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR')

class ClockButton(Button):

	def __init__(self,*args,**kwargs):
		super(ClockButton,self).__init__(*args,**kwargs)
		Clock.schedule_interval(self.update, 1)

	def update(self, *args):
		self.text = str(datetime.datetime.now())
		self.color = [0.2,0.5,0.9,1]
		print(self.text)
