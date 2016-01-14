
from kivy.app import App
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, FallOutTransition

import time
import random

class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class MyScreenManager(ScreenManager):
    pass


class ScreenManagerApp(App):
    def build(self):
        screen=MyScreenManager()
        screen.add_widget(FirstScreen())
        screen.add_widget(SecondScreen())
        return screen

if __name__ == "__main__":
    ScreenManagerApp().run()
