from kivy.app import App

from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import subprocess


class ScatterTextWidget(BoxLayout):
	pass

class TutorialApp(App):

	def build(self):
		self.playing = False
		return ScatterTextWidget()

	def toggle_radio(self):
		print('bouton presse')
		if self.playing:
			subprocess.check_output(["mpc","stop"])
			self.playing = False
		else:
			subprocess.check_output(["mpc","play","1"])
			self.playing = True


if __name__ == "__main__":
	TutorialApp().run()