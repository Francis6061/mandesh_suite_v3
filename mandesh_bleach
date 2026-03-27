import requests
from colorama import Fore, Style

def check_breach(query):
    print(f"{Fore.YELLOW}[*] Diving into leaked databases for: {query}...{Style.RESET_ALL}")
    
    # Using LeakCheck's public API endpoint
    url = f"https://leakcheck.net/api/public?check={query}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("success") and data.get("found") > 0:
            print(f"{Fore.RED}[!] WARNING: {data['found']} breaches found!{Style.RESET_ALL}")
            for leak in data.get("sources", []):
                print(f"{Fore.WHITE}  - Source: {leak['name']} ({leak['date']}){Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] Clean: No public breaches found for this entry.{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}[!] API Connection Error: {e}{Style.RESET_ALL}")

# Example: check_breach("target_email@gmail.com")
