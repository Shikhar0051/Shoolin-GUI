import requests

def search_hackertarget(self, target):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36', }
    params = (('q', target),)

    res = requests.get('https://api.hackertarget.com/hostsearch/', headers=headers, params=params)

    res = res.text.split('\n')
    for item in res:
        try:
            if item.split(",")[0] != "":
                domain = item.split(",")[0]
                domain = domain.strip()
                if domain not in self.domains and domain.endswith("." + target):
                    self.domains.append(domain)
        except Exception:
            self.errors.append("Error in Hackertarget")
    
    