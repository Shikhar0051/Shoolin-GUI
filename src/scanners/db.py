from json import dumps, loads
import requests

def search_db(self, target):
    res = requests.get("https://jonlu.ca/anubis/subdomains/" + target)

    if res.status_code == 200 and res.text:
        subdomains = loads(res.text)
        for domain in subdomains:
            if domain not in self.domains:
                self.domains.append(domain)

                