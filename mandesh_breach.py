import requests
from colorama import Fore, Style

def check_breach(query):
    print(f"{Fore.YELLOW}[*] Diving into leaked databases for: {query}...{Style.RESET_ALL}")
    
    # Using the LeakCheck Public API (No key required for basic checks)
    url = f"https://leakcheck.net/api/public?check={query}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get("success") and data.get("found", 0) > 0:
            print(f"{Fore.RED}[!] WARNING: {data['found']} breaches found!{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'Source':<25} | {'Date'}{Style.RESET_ALL}")
            print("-" * 40)
            
            for leak in data.get("sources", []):
                name = leak.get('name', 'Unknown')
                date = leak.get('date', 'Unknown')
                print(f"{Fore.LIGHTRED_EX}{name:<25} | {date}{Style.RESET_ALL}")
                
            print(f"\n{Fore.CYAN}[*] Use these sources to pivot your search on Social Recon.{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] Clean: No public breaches found for this entry.{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Connection Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.BLUE}--- Mandesh Breach Diver ---{Style.RESET_ALL}")
    target = input("Enter Email or Username: ")
    if target:
        check_breach(target)
    else:
        print("Invalid Input.")
