import socket
from json import dumps
import shodan

def search_shodan(self, target):
    api = shodan.Shodan("PGHgSzfOUl5UJ44qJ53f7tZn9gQwvwIM")
    lp = {}
    
    try:
        ip = socket.gethostbyname(target)
        res = api.host(ip)
        lp['ip'] = ip
        lp['server_location'] = str(res['city'])
        lp['country_code'] = str(res['country_code'])
        lp['postal_code'] = str(res['postal_code'])
        lp['isp'] = str(res['isp'])
        if res['os'] is not None:
            lp['os'] = str(res['os'])

        
    except Exception:
        self.errors.append("Error in shodan")

    if len(lp) > 0:
        self.shodan_info.append(lp)