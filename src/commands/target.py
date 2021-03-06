import threading
import socket

from src.scanners.crt import search_crtsh
from src.scanners.dnsdumpster import search_dnsdumpster
from src.scanners.hackertarget import search_hackertarget
from src.scanners.netcraft import search_netcraft
from src.scanners.ssl import search_ssl_alt_names
from src.scanners.zonetransfer import search_zonetransfer
from src.scanners.nmap import scan_hosts
from src.scanners.db import search_db
from src.scanners.shodan import search_shodan

class Target():
    domains = list()
    errors = list()
    ded = set()
    zonetransfers = list()
    nmap_result = {}
    ip = str()
    shodan_info = []

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        
    def run(self):
        self.domains = []
        self.errors = []
        self.ded = set()
        self.zonetransfers = []
        self.nmap_result = {}
        self.ip = str()
        self.shodan_info = []
        
        for target in self.options['--target']:
            try:
                self.ip.append(socket.gethostbyname(target))
            except Exception:
                self.errors.append("Error in getting host ip")

            threads = [threading.Thread(target=search_crtsh, args=(self, target)),
                        threading.Thread(target=search_dnsdumpster, args=(self, target)),
                        threading.Thread(target=search_hackertarget, args=(self, target)),
                        threading.Thread(target=search_netcraft, args=(self, target)),
                        threading.Thread(target=search_ssl_alt_names, args=(self, target)),
                        threading.Thread(target=search_zonetransfer, args=(self, target)),
                        threading.Thread(target=search_db, args=(self, target))]
            try:
                if self.options["--with-nmap"]:
                    threads.append(threading.Thread(target=scan_hosts, args=(self, self.options["--overwrite-nmap-scan"])))
                
                if self.options["--additional-info"]:
                    threads.append(threading.Thread(target=search_shodan, args=(self, target)))
            
            except Exception:
                pass

            for x in threads:
                x.start()
            
            for x in threads:
                x.join()

            self.domains = self.clean_domains(self.domains)
            self.ded = set(self.domains)

        return {'results': self.ded, 'zonetransfer': self.zonetransfers, "nmap": self.nmap_result}
    
    def clean_domains(self, domains):
        clean = []
        for sub in domains:
            sub = sub.lower()
            if sub.find('//') != -1:
                sub = sub[sub.find("//") + 2:]
            
            if sub.endswith('.'):
                sub = sub[:-1]
            
            if sub[0] in ["\\", ".", "/", "#", "$", "%"]:
                sub = sub[1:]
            
            if "@" in sub:
                sub = sub.split("@")
                
                if len(sub) > 1:
                    sub = sub[1]
                else:
                    sub = sub[0]

            clean.append(sub.strip())
        return clean