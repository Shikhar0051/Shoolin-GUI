# Shoolin GUI
This is a GUI based free subdomain enumeration tool that collects subdomain data from various online resources and present it in a sequential manner. 
<br>Subdomain enumeration is one of the first steps in the information gathering phase, and is required to get a full scope of the attack surfaces of your target.

## Getting Started

### Prerequisites

* Nmap (if wanting to run port scans and certain certificate scans)
* Check the nmap using 'nmap' command. If not present, download Nmap from <a href='https://nmap.org/download.html'> Nmap Website </a>


### Installation
It is preferable to create a virtual environment before installing the requirements.
```
git clone https://github.com/Shikhar0051/Shoolin-GUI.git
cd Shoolin-GUI
pip install  -r requirements.txt
pip install .
```

If any problem is encountered while installing kivy, please follow the given code.
```
python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer
python -m pip install kivy.deps.angle
python -m pip install pygame
python -m pip install kivy
```

Run the `requirements.txt` file again to install other package dependencies.

## Usage

Run the `Shoolin_GUI.py` file to execute the code. 

It is a simple to use GUI tool. It is necessary to provide a specific target or a target file to run the application. The output data will be gathered and presented in the output window. A navigable button is provided to traverse between the screens.

![shoolin_main](https://user-images.githubusercontent.com/48147323/124134435-75bee780-daa0-11eb-9b92-9fa6dedd2b21.png)


![image](https://user-images.githubusercontent.com/48147323/124134386-69d32580-daa0-11eb-989a-4df326bd3075.png)


## Contributing
Read the [Contributing.md](https://github.com/Shikhar0051/Shoolin-GUI/blob/master/contributing.md) file before contributing or opening an issue.
