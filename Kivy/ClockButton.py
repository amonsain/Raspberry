from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from time import gmtime, strftime, localtime
import locale

locale.setlocale(locale.LC_ALL, 'fr_FR')

class ClockButton(Button):

	def __init__(self,*args,**kwargs):
		super(ClockButton,self).__init__(*args,**kwargs)
		Clock.schedule_interval(self.update, 1)

	def update(self, *args):
		self.text = '[b]'+ strftime("%d %b %H:%M:%S", localtime())+'[/b]'
		self.markup=True
		self.color = [0.2,0.5,0.9,1]
		print(self.text)
