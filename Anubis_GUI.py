import sys
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.window import Window

Window.size = (600, 600)

class HelpWindow(Screen):
    """
    This is a help window. It contains the functionality of all the given boxes
    on the main window.
    """

    def main_window(self):
        sm.current = "main"

class MainWindow(Screen):
    """
    This is the main window that contains the main form.
    This connects the frontend of the app to the backend
    """

    target = ObjectProperty(None)
    out_file = ObjectProperty(None)
    overwrite_nmap = ObjectProperty(None)
    with_nmap = ObjectProperty(None)
    add_info = ObjectProperty(None)
    ip = ObjectProperty(None)
    recursive = ObjectProperty(None)
    ssl = ObjectProperty(None)
    silent = ObjectProperty(None)
    verbrose = ObjectProperty(None)
    anubis_db = ObjectProperty(None)

    def v_popup(self):
        version_popup()
    
    def help(self):
        sm.current = "help"
    
    def output_window(self):
        sm.current = "output"

    def get_results(self):
        if self.target.text == "" :
            invalid_target("target not specified")

    def reset_window(self):
        self.target.text = ""
        self.out_file.text = ""
        self.overwrite_nmap.text = ""
        self.with_nmap.active = False
        self.add_info.active = False
        self.ip.active = False
        self.ssl.active = False
        self.silent.active = False
        self.recursive.active = False
        self.verbrose.active = False
        self.anubis_db.active = False

class OutputWindow(Screen):
    """
    This is the output window. All the generated results will be seen here.
    """

    def main_window(self):
        sm.current = "main"

class WindowManager(ScreenManager):
    pass

def version_popup():
    """
    Version Popup Window.
    """
    
    version = "v1.0"
    version_text = "this is "+version+" for this app"
    vpop = Popup(title="Version",
                    content=Label(text=version_text),
                    size_hint=(None, None), size=(400, 400))
    
    vpop.open()

def invalid_target(rep):
    """
    Invalid form popup.
    """
    
    vpop = Popup(title="Invalid Parameters!",
                    content=Label(text=rep),
                    size_hint=(None, None), size=(400, 400))
    
    vpop.open()

### main builder and WindowManager object
kv = Builder.load_file("start.kv")
sm = WindowManager()

### Adding screens to widget
screens = [MainWindow(name="main"), HelpWindow(name="help"), OutputWindow(name="output")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"

### main working
class AnubisApp(App):
    def build(self):
        return sm
        
if __name__ == '__main__':
    AnubisApp().run()