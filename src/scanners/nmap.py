from json import dumps
import nmap

def scan_hosts(self, arguments):
    nm = nmap.PortScanner()
    
    nm.scan(hosts=self.ip, arguments=arguments)
    arr = []
    for host in nm.all_hosts():
        arr.append(dumps(nm[host], indent=2, sort_keys=True))
        
        self.nmap_result["all_results"].append(arr)

        for proto in nm[host].all_protocols():
            continue
        self.nmap_result["protocol"] = proto

        lp = {
            'port': "",
        }
        lport = nm[host][proto].keys()
        for port in lport:
            lp['port'] = port
            try:
                if nm[host][proto][port]['product']:
                    lp['service'] = nm[host][proto][port]['product']
                if nm[host][proto][port]['version']:
                    lp['port'] = nm[host][proto][port]['version']
                self.nmap_result['port_info'].append(lp)
            except Exception as e:
                print(e)

            try:
                fix_newline = nm[host][proto][port]['script']['ssl-cert'].split('\n')
                
                for i in range(len(fix_newline)):
                    
                    if fix_newline[i].startswith("Subject Alternative Name: "):
                        content = fix_newline[i].replace("Subject Alternative Name: ", '')
                        content = content.replace("DNS:", '')
                        new_domains = content.split(",")
                        for domain in new_domains:
                            domain = domain.strip()
                            if domain not in self.domains:
                                self.domains.append(domain)
                                
            except Exception:
                continue   
