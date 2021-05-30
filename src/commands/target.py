import threading
from src.scanners.crt import search_crtsh

class Target():
    domains = list()
    errors = list()
    ded = set()

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

        
    def run(self):
        for target in self.options['--target']:
            threads = [threading.Thread(target=search_crtsh, args=(self, target))]

            for x in threads:
                x.start()
                
            if len(self.errors) > 1:
                return self.errors
            
            for x in threads:
                x.join()

            self.domains = self.clean_domains(self.domains)
            self.ded = set(self.domains)

        return self.ded
    
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