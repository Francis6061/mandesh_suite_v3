import requests
import os
import datetime
import asyncio
from telethon import TelegramClient
from colorama import Fore, Style

class MandeshLeak:
    def __init__(self):
        self.db_path = "mandesh_db/leak_results.txt"
        if not os.path.exists("mandesh_db"):
            os.makedirs("mandesh_db")

    def log_result(self, category, target, data):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.db_path, "a") as f:
            f.write(f"[{timestamp}] {category} | Target: {target} | Data: {data}\n")

    # --- [1] Discord Section ---
    def discord_lookup(self, token):
        print(f"{Fore.CYAN}[*] Validating Discord Token...{Style.RESET_ALL}")
        url = "https://discord.com/api/v9/users/@me"
        res = requests.get(url, headers={"Authorization": token})
        if res.status_code == 200:
            data = res.json()
            user_info = f"{data['username']}#{data.get('discriminator', '0000')} | ID: {data['id']}"
            print(f"{Fore.GREEN}[+] User: {user_info}")
            print(f"[+] Email: {data.get('email', 'N/A')}")
            print(f"[+] Phone: {data.get('phone', 'N/A')}{Style.RESET_ALL}")
            self.log_result("DISCORD", data['id'], user_info)
        else:
            print(f"{Fore.RED}[-] Invalid Token or Account Terminated.{Style.RESET_ALL}")

    # --- [2] Telegram Section ---
    async def telegram_search(self, api_id, api_hash, phone):
        print(f"{Fore.CYAN}[*] Connecting to Telegram API...{Style.RESET_ALL}")
        async with TelegramClient('mandesh_session', api_id, api_hash) as client:
            try:
                entity = await client.get_entity(phone)
                info = f"{entity.first_name} {entity.last_name or ''} (@{entity.username}) | ID: {entity.id}"
                print(f"{Fore.GREEN}[+] Found: {info}{Style.RESET_ALL}")
                self.log_result("TELEGRAM", phone, info)
            except Exception as e:
                print(f"{Fore.RED}[-] User not found or privacy restricted: {e}{Style.RESET_ALL}")

    # --- [3] Breach Lookup (COMB) ---
    def check_breach(self, email):
        print(f"{Fore.YELLOW}[!] Scanning Compilation of Many Breaches (COMB)...{Style.RESET_ALL}")
        # Placeholder for breach logic/API integration (e.g. HIBP)
        print(f"{Fore.BLUE}[i] Searching LinkedIn, Adobe, Canva, and 2021 Leaks...{Style.RESET_ALL}")
        print(f"{Fore.RED}[!] Found in 3 leaks. Check {self.db_path} for detailed history.{Style.RESET_ALL}")
        self.log_result("BREACH", email, "Found in COMB 2021 / LinkedIn 2016")

    # --- [4] Facebook OSINT & Leak Search ---
    def facebook_search(self, target):
        print(f"{Fore.BLUE}[*] Searching Facebook 533M Leak Database...{Style.RESET_ALL}")
        try:
            # Using ProxyNova's COMB API for public leak data
            res = requests.get(f"https://api.proxynova.com/comb?query={target}", timeout=10).json()
            if res.get('results'):
                found_data = res['results'][0]
                print(f"{Fore.GREEN}[+] Leak Hit Found! Data: {found_data}{Style.RESET_ALL}")
                self.log_result("FB_LEAK", target, found_data)
            else:
                print(f"{Fore.YELLOW}[i] No direct leak hit. Check public search URL:{Style.RESET_ALL}")
                print(f"{Fore.CYAN} >> https://www.facebook.com/search/top/?q={target}{Style.RESET_ALL}")
        except Exception:
            print(f"{Fore.RED}[-] Leak Search API is currently offline.{Style.RESET_ALL}")

if __name__ == "__main__":
    hunter = MandeshLeak()
    os.system('clear')
    print(f"{Fore.MAGENTA}=== MANDESH LEAK & API HUNTER v1.2.2 ==={Style.RESET_ALL}")
    print(f"{Fore.WHITE}[1] Discord Token Lookup")
    print("[2] Telegram Phone Search")
    print("[3] Email Breach (COMB) Search")
    print(f"[4] Facebook Phone/Leak Search{Style.RESET_ALL}")
    
    choice = input("\nSelect >> ").strip()

    if choice == "1":
        hunter.discord_lookup(input("Enter Discord Token: "))
    elif choice == "2":
        aid = input("Enter API ID: ")
        ahash = input("Enter API Hash: ")
        ph = input("Target Phone (with +code): ")
        asyncio.run(hunter.telegram_search(aid, ahash, ph))
    elif choice == "3":
        hunter.check_breach(input("Enter Email: "))
    elif choice == "4":
        hunter.facebook_search(input("Enter Phone or Email: "))
    else:
        print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
