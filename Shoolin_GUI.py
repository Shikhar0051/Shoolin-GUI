import os
import re
from kivy.clock import Clock
from urllib.parse import urlsplit
import requests
import webbrowser

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.factory import Factory
from plyer import filechooser
from kivy.config import Config
from collections import defaultdict as dt
from src.commands.target import Target
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

Window.size = (600, 400)
Config.set('graphics', 'resizable', False) #0 being off 1 being on as in true/false

VERSION = "v1.0"
Update = False

class HelpWindow(Screen):
    """
    This is a help window. It contains the functionality of all the given boxes
    on the main window.
    """
    update_software = ObjectProperty(None)

    def get_software_page(self):
        if Update == False:
            vpop = Popup(title="No Updates",
                    content=Label(text="Update Not Available"),
                    size_hint=(None, None), size=(300, 300))
    
            vpop.open()

    def get_github(self):
        webbrowser.open("https://github.com/Shikhar0051/Shoolin-GUI")

    def main_window(self):
        sm.current = "main"

def check_for_updates():
    try:
        res = requests.get("https://shikhargupta.me/assets/versionInfo/version")
        if res.status_code == 200:
            if res.text != VERSION:
                update_available()
        else:
            #error_confirm("Unable to check for updates")
            pass
    except Exception:
        no_internet()

class MainWindow(Screen):
    """
    This is the main window that contains the main form.
    This connects the frontend of the app to the backend
    """

    Clock.schedule_once(lambda dt: check_for_updates())
    
    target = ObjectProperty(None)
    out_file = ObjectProperty(None)
    overwrite_nmap = ObjectProperty(None)
    with_nmap = ObjectProperty(None)
    add_info = ObjectProperty(None)
    ip = ObjectProperty(None)
    recursive = ObjectProperty(None)
    ssl = ObjectProperty(None)
    verbrose = ObjectProperty(None)
    uploaded_file = ObjectProperty(None)
    file_choosen = ObjectProperty(None)

    file_path = ""
    file_name = ""
    output_file = False

    def v_popup(self):
        version_popup()
    
    def help(self):
        sm.current = "help"
    
    def output_window(self):
        sm.current = "output"

    def get_results(self):
        if self.target.text == "" and self.file_path == "":
            invalid_popup("target not specified")
        elif self.target.text and self.file_path:
            invalid_popup("Please select either Target or Target File")
            self.file_choosen.visible = True
            self.target.text = ""
        else:
            options = {}
            if self.target.text != "":
                options["--target"] = self.target.text
                options["--target"] = list(filter(None, options["--target"].split(",")))
                
            else:
                f = open(self.file_path, "r")
                items = []
                for item in f.readlines():
                    item = item.replace("\n", "")
                    items.append(item)
                options["--target"] = items

            print(options)
            for i in range(len(options["--target"])):
                url = options["--target"][i]
                # Inject protocol if not there
                if not re.match(r'http(s?):', url):
                    url = 'http://' + url

                parsed = urlsplit(url)
                host = parsed.netloc
                options["--target"][i] = host
            
            if self.out_file.text != "":
                file = self.out_file.text
                if file[-4:] != ".txt":
                    file+=".txt"
                options["--output"] = file
                self.output_file = True
            
            if self.overwrite_nmap.text != "" or self.with_nmap.active:
                options["--with-nmap"] = True
                if self.overwrite_nmap.text == "":
                    options["--overwrite-nmap-scan"] = "-nPn -sV -sC"
                else:
                    options["--overwrite-nmap-scan"] = self.overwrite_nmap.text
            
            if self.file_path != "":
                options["--file"] = self.file_path
            
            if self.ssl.active:
                options["--ssl"] = True
            
            if self.add_info.active:
                options["--additional-info"] = True
            
            if self.recursive.active:
                options["--recursive"] = True

            #OutputWindow.main(options = options)
            if self.output_file:
                command = Target(options)
                result = command.run()
                save_path = "./output/"
                complete = os.path.join(save_path, options["--output"])
                f = open(complete, "w")

                for item in result["results"]:
                    f.write(item + "\n")
                
                file_saved(complete)
                self.reset_window()

            else:
                out_window = self.manager.get_screen('output')
                out_window.main(options)
                sm.current = "output"
    
    def get_file(self):
        path = filechooser.open_file(title="Pick a text file..", 
                             filters=[("Comma-separated Values", "*.txt")])
        
        if len(path)==1:
            p = path[0]
            self.file_path = p
            p = list(map(str, p.split("\\")))
            self.file_name = p[-1]
            self.uploaded_file.text = self.file_name

            self.file_choosen.visible = False
        else:
            invalid_popup("Please choose a single text file")

    def reset_window(self):
        self.target.text = ""
        self.out_file.text = ""
        self.overwrite_nmap.text = ""
        self.with_nmap.active = False
        self.add_info.active = False
        self.ssl.active = False
        self.recursive.active = False
        self.file_choosen.visible = True
        self.file_path = ""

class OutputWindow(Screen):
    """
    This is the output window. All the generated results will be seen here.
    """
    res = ObjectProperty(None)
    res_out = ObjectProperty(None)

    def main(self, options):
        try:
            print(options)
            command = Target(options)
            result = command.run()
            print(result)
            
            for item in result['results']:
                self.res_out.add_widget(Label(size_hint_y=None,height=20,text=item))
                if len(result['zonetransfer'])>0:
                    for item in result['zonetransfer']:
                        self.res_out.add_widget(Label(size_hint_y=None,height=20,text=item))
                if len(result['zonetransfer'])>0:
                    for item in result['nmap']:
                        self.res_out.add_widget(Label(size_hint_y=None,height=20,text=item))

        except Exception as e:
            error_popup("Error Occured!")
            print(e)
        self.main_window()


    def main_window(self):
        sm.current = "main"

class WindowManager(ScreenManager):
    pass



def version_popup():
    """
    Version Popup Window.
    """
    
    version = VERSION
    version_text = "this is "+version+" for this app"
    vpop = Popup(title="Version",
                    content=Label(text=version_text),
                    size_hint=(None, None), size=(300, 300))
    
    vpop.open()

def invalid_popup(rep):
    """
    Invalid form popup.
    """
    
    vpop = Popup(title="Invalid Parameters!",
                    content=Label(text=rep),
                    size_hint=(None, None), size=(300, 300))
    
    vpop.open()

def error_popup(rep):
    """
    Invalid form popup.
    """
    
    vpop = Popup(title="Error!",
                    content=Label(text=rep),
                    size_hint=(None, None), size=(300, 300))
    
    vpop.open()


def file_saved(rep):
    """
    File Saved popup.
    """
    res = "File Saved successfully!! \nLocation = " + rep
    vpop = Popup(title="File Saved successfully",
                    content=Label(text=res),
                    size_hint=(None, None), size=(300, 300))
    
    vpop.open()

def update_available():
    box = GridLayout(cols=1)
    box.add_widget(Label(text="Update Available"))
    global Update 
    Update = True
    vpop = Popup(title="Please update the software",
                    content=box,
                    size_hint=(None, None), size=(300, 300))
    
    vpop.open()

def no_internet():
    box = GridLayout(cols=1)
    box.add_widget(Label(text="""No Internet... \nPlease check your connection \nand try again."""))
    
    vpop = Popup(title="No Internet Connection",
                    content=box,
                    size_hint=(None, None), size=(300, 300),
                    auto_dismiss = False)
    
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
class ShoolinApp(App):
    def build(self):
        return sm
        
if __name__ == '__main__':
    ShoolinApp().run()