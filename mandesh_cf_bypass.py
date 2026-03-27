import socket
import requests
from colorama import Fore, Style

def bypass_logic(domain):
    print(f"{Fore.CYAN}[*] Attempting to find Real IP for: {domain}{Style.RESET_ALL}")
    
    # Common "forgotten" subdomains that often point to the real server
    subdomains = ['direct-connect', 'direct', 'ftp', 'cpanel', 'mail', 'dev', 'staging']
    
    found_ips = set()
    
    for sub in subdomains:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            # Check if the resolved IP belongs to Cloudflare
            # Simple check: Cloudflare usually owns specific ranges
            print(f" {Fore.YELLOW}[?] Testing {target} -> {ip}{Style.RESET_ALL}")
            found_ips.add(ip)
        except socket.gaierror:
            continue

    if found_ips:
        print(f"\n{Fore.GREEN}[!] Potential Origin IPs Found:{Style.RESET_ALL}")
        for ip in found_ips:
            print(f" [>] {ip}")
    else:
        print(f"{Fore.RED}[!] No direct IPs discovered.{Style.RESET_ALL}")

def cf_main():
    print(f"{Fore.MAGENTA}=== MANDESH CLOUDFLARE BYPASS [13] ==={Style.RESET_ALL}")
    domain = input("Enter Target Domain (e.g., victim.com): ").replace("http://", "").replace("https://", "").strip("/")
    bypass_logic(domain)

if __name__ == "__main__":
    cf_main()
