from collections import defaultdict
import socket
import ssl

def search_ssl_alt_names(self, target):
    try:
        context = ssl.create_default_context()

        try:
            with socket.create_connection((target, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
            
            alt_name = defaultdict(set)
            
            for type_, san in cert['subjectAltName']:
                alt_name[type_].add(san)

            dns_domains = list(alt_name['DNS'])
            for domain in dns_domains:
                if domain:
                    self.domains.append(domain.strip())

        except Exception:
            self.errors.append("Error connecting Targets")
    
    except Exception:
        self.errors.append("Error in ssl")