from src.scanners.crt import search_crtsh

class Target():
    domains = list()

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def handle_exception(self, error):
        return error
        
    def run(self):
        pass