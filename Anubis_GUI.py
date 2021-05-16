import sys
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class HelpWindow(Screen):
    pass

class MainWindow(Screen):
    pass

class OutputWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

def version_popup():
    version = "v1.0"
    version_text = "this is "+version+" for this app"
    vpop = Popup(title="Version",
                    content=Label(text=version_text),
                    size_hint=(None, None), size=(400, 400))
    
    vpop.open()

def invalid_target():
    rep = "Invalid Parameters"
    vpop = Popup(title="Invalid Parameters!",
                    content=Label(text=rep),
                    size_hint=(None, None), size=(400, 400))
    
    vpop.open()

kv = Builder.load_file("start.kv")
sm = WindowManager()

screens = [MainWindow(name="main"), HelpWindow(name="help"), OutputWindow(name="output")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

class AnubisApp(App):
    def build(self):
        return sm
        

if __name__ == '__main__':
    AnubisApp().run()