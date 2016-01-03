from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button



class ScatterTextWidget(BoxLayout):
	pass

class TutorialApp(App):
	def build(self):
		return ScatterTextWidget()

	def play_radio(self):
		print('bouton presse')

if __name__ == "__main__":
	TutorialApp().run()