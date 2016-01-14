from kivy.clock import Clock
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class MainLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        self.layout = MainLayout()
        self.label = Label(text = "john")
        self.layout.add_widget(self.label)
        self.current_i = 0
        Clock.schedule_interval(self.update,0.1)
        return self.layout

    def update(self, *args):
        self.label.text = str(self.current_i)
        self.current_i += 1
        if self.current_i >= 50:
            Clock.unschedule(self.update)

if __name__ == "__main__":
    MyApp().run()