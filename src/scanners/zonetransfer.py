import socket
import dns.query
import dns.resolver
import dns.zone

def search_zonetransfer(self, target):
    resolver = dns.resolver.Resolver()

    try:
        answers = resolver.query(target, 'NS')
    except Exception:
        self.errors.append("Error checking for Zone Transfers")

    resolved_ips = []

    for ns in answers:
        ns = str(ns).rstrip('.')
        resolved_ips.append(socket.gethostbyname(ns))
    
    for ip in resolved_ips:
        try:
            zone = dns.zone.from_xfr(dns.query.xfr(ip, target))
            for name, node in zone.nodes.items():
                name = str(name)
                if name not in ["@", "*"]:
                    self.zonetransfers.append(name + '.' + target)
        except Exception:
            self.errors.append("Error in dns query in ZoneTransfer")