import threading

from src.scanners.crt import search_crtsh
from src.scanners.dnsdumpster import search_dnsdumpster
from src.scanners.hackertarget import search_hackertarget
from src.scanners.netcraft import search_netcraft
from src.scanners.ssl import search_ssl_alt_names
from src.scanners.zonetransfer import search_zonetransfer

class Target():
    domains = list()
    errors = list()
    ded = set()
    zonetransfers = list()

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        
    def run(self):
        self.domains = []
        self.errors = []
        self.ded = set()
        self.zonetransfers = []
        
        for target in self.options['--target']:
            threads = [threading.Thread(target=search_crtsh, args=(self, target)),
                        threading.Thread(target=search_dnsdumpster, args=(self, target)),
                        threading.Thread(target=search_hackertarget, args=(self, target)),
                        threading.Thread(target=search_netcraft, args=(self, target)),
                        threading.Thread(target=search_ssl_alt_names, args=(self, target)),
                        threading.Thread(target=search_zonetransfer, args=(self, target))]

            for x in threads:
                x.start()
                
            if len(self.errors) > 1:
                return self.errors
            
            for x in threads:
                x.join()

            self.domains = self.clean_domains(self.domains)
            self.ded = set(self.domains)

        return [self.ded, self.zonetransfers]
    
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