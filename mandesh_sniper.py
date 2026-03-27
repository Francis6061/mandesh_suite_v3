
import requests
from colorama import Fore, Style

def snipe_subdomains():
    print(f"{Fore.CYAN}=== MANDESH SUBDOMAIN SNIPER v1.2.2 ==={Style.RESET_ALL}")
    domain = input("Enter Target Domain (e.g., google.com): ").strip()
    
    # List of common subdomains to check
    subs = ['www', 'mail', 'ftp', 'localhost', 'dev', 'api', 'admin', 'portal', 
            'test', 'vps', 'support', 'webmail', 'server', 'blog', 'crm']
    
    print(f"[*] Scanning {len(subs)} common subdomains for {domain}...\n")
    
    found_count = 0
    for sub in subs:
        url = f"http://{sub}.{domain}"
        try:
            # Use a 3-second timeout to keep the scan fast
            response = requests.get(url, timeout=3)
            if response.status_code < 400:
                print(f"{Fore.GREEN}[+] FOUND: {url} (Status: {response.status_code}){Style.RESET_ALL}")
                found_count += 1
        except requests.ConnectionError:
            continue
        except requests.Timeout:
            continue
            
    print(f"\n{Fore.YELLOW}[*] Scan Complete. Found {found_count} active subdomains.{Style.RESET_ALL}")

if __name__ == "__main__":
    snipe_subdomains()



'''import requests

def scan_subdomains(domain, wordlist_path):
    print(f"[*] Starting Subdomain Sniper on: {domain}")
    with open(wordlist_path, 'r') as file:
        for line in file:
            sub = line.strip()
            url = f"http://{sub}.{domain}"
            try:
                # We use a short timeout (2s) to keep the scan fast
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    print(f"[+] Found Live Subdomain: {url}")
            except requests.ConnectionError:
                pass
            except Exception as e:
                pass

# Usage example
# scan_subdomains("egerton.ac.ke", "subdomains_ke.txt")
'''

