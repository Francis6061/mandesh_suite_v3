import os, socket, requests, nmap
from colorama import Fore, Style

def dns_recon(domain):
    print(f"\n{Fore.BLUE}[*] EXTENDED DNS RECONNAISSANCE{Style.RESET_ALL}")
    records = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    for rec in records:
        print(f"{Fore.CYAN}[{rec} Record]:{Style.RESET_ALL}")
        os.system(f"host -t {rec} {domain} | grep 'has address\|record\|handled by'")

def subdomain_brute(domain):
    print(f"\n{Fore.YELLOW}[*] QUICK SUBDOMAIN SCAN{Style.RESET_ALL}")
    # Common subdomains for quick discovery
    subs = ['www', 'mail', 'ftp', 'admin', 'dev', 'cpanel', 'webmail', 'api']
    for s in subs:
        url = f"{s}.{domain}"
        try:
            ip = socket.gethostbyname(url)
            print(f" {Fore.GREEN}[+] Found: {url} -> {ip}{Style.RESET_ALL}")
        except socket.gaierror:
            continue

def get_geo_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        print(f"\n{Fore.MAGENTA}[*] GEOGRAPHIC INTELLIGENCE")
        print(f" [+] ISP: {res.get('isp')}\n [+] Org: {res.get('org')}\n [+] Location: {res.get('city')}, {res.get('country')}{Style.RESET_ALL}")
    except:
        print(f"{Fore.RED}[!] Could not fetch Geo-IP data.{Style.RESET_ALL}")

def audit_main():
    print(f"{Fore.RED}=== MANDESH AUDITOR v1.2.2 (RED HAWK MODE) ==={Style.RESET_ALL}")
    target = input("Enter Domain (eg. google.com): ").replace("https://", "").replace("http://", "").strip("/")
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{Fore.GREEN}[!] Target IP: {target_ip}{Style.RESET_ALL}")
        
        get_geo_info(target_ip)
        dns_recon(target)
        subdomain_brute(target)
        
        # Optional: Add Nmap call from previous step here
    except Exception as e:
        print(f"{Fore.RED}[!] Target Resolve Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    audit_main()





###########
'''import socket
import requests
import whois
import dns.resolver
from colorama import Fore, Style
from mandesh_utils import save_result

class MandeshAudit:
    def __init__(self, target):
        self.target = target.replace("https://", "").replace("http://", "").split('/')[0]
        self.log_data = [] # To store results for saving
        self.log(f"\n{Fore.YELLOW}[!] Auditing: {self.target}{Style.RESET_ALL}")

    def log(self, text):
        """Prints text and adds it to the log buffer (without colors)."""
        print(text)
        # Strip ANSI colors for the saved file
        clean_text = text.replace(Fore.YELLOW, "").replace(Fore.GREEN, "").replace(Fore.RED, "") \
                         .replace(Fore.CYAN, "").replace(Fore.MAGENTA, "").replace(Fore.BLUE, "") \
                         .replace(Style.RESET_ALL, "").replace(Fore.WHITE, "")
        self.log_data.append(clean_text)

    def get_ip(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.log(f"{Fore.GREEN}[+] IP Address: {ip}{Style.RESET_ALL}")
            return ip
        except:
            self.log(f"{Fore.RED}[-] Could not resolve IP{Style.RESET_ALL}")

    def check_cloudflare(self):
        try:
            headers = requests.get(f"http://{self.target}", timeout=5).headers
            if 'CF-RAY' in headers or ('server' in headers and 'cloudflare' in headers.lower()):
                self.log(f"{Fore.MAGENTA}[+] Cloudflare Detected: Real IP might be hidden{Style.RESET_ALL}")
            else:
                self.log(f"{Fore.BLUE}[-] No Cloudflare detected{Style.RESET_ALL}")
        except: pass

    def dns_recon(self):
        self.log(f"{Fore.CYAN}[*] Fetching DNS Records...{Style.RESET_ALL}")
        for record in ['A', 'MX', 'NS', 'TXT']:
            try:
                answers = dns.resolver.resolve(self.target, record)
                for rdata in answers:
                    self.log(f"  [{record}] {rdata}")
            except: pass

    def scan_common_ports(self):
        common_ports = [21, 22, 80, 443, 3306, 8080]
        self.log(f"{Fore.CYAN}[*] Scanning Common Ports...{Style.RESET_ALL}")
        for port in common_ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.target, port))
            if result == 0:
                self.log(f"  [+] Port {port} is OPEN")
            s.close()

if __name__ == "__main__":
    target_input = input("Enter target (domain/IP): ")
    auditor = MandeshAudit(target_input)
    auditor.get_ip()
    auditor.check_cloudflare()
    auditor.dns_recon()
    auditor.scan_common_ports()
    
    # Final step: Trigger the save utility
    report = "\n".join(auditor.log_data)
    save_result("AUDITOR", report)
'''

