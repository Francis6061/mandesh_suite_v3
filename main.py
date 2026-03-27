import os
import sys
from colorama import Fore, Style

# Updated Import Safety Check
try:
    import mandesh_phish, mandesh_pi, mandesh_audit, mandesh_payload
    import mandesh_bomber, mandesh_crack, mandesh_webscan, mandesh_leak
    import mandesh_sys, mandesh_exif, mandesh_sniper, mandesh_hunt
    import mandesh_cf_bypass, mandesh_google_dorking, mandesh_report
except ImportError as e:
    print(f"{Fore.RED}[!] Missing module: {e}. Check your directory!{Style.RESET_ALL}")

class MandeshGUI:
    def __init__(self):
        self.version = "1.2.2"
        self.author = "Francis Macharia Nderu"

    def banner(self):
        os.system('clear')
        print(f"""{Fore.RED}
  __  __                  _             _   _   _       _   _       
 |  \/  |                | |           | | | | | |     | | (_)      
 | \  / | __ _ _ __   __| | ___| ___| |__ | |_| | __ _| | ___ _ _ __  
 | |\/| |/ _` | '_ \ / _` |/ _ \/ __| '_ \|  __  |/ _` | |/ / | | '_ \ 
 | |  | | (_| | | | | (_| |  __/\__ \ | | | |  | | (_| |  <| | | | | |
 |_|  |_|\__,_|_| |_|\__,_|\___||___/_| |_|_|  |_|\__,_|_|\_\_|_|_| |_|
        {Fore.YELLOW}>> Pro OSINT & Pentest Suite v{self.version} | Author: {self.author}{Style.RESET_ALL}
        """)

    def authenticate(self):
        # Quick bypass for development: enter 'admin' and 'mandesh'
        user = input("Username: ")
        pw = input("Password: ")
        return user == "admin" and pw == "mandesh"

    def menu(self):
        while True:
            self.banner()
            # Layout organized for high-resolution and mobile terminal views
            print(f"{Fore.CYAN}[01] Phishing Engine      [07] Security Cracker")
            print(f"[02] Intelligence Hub      [08] Web Vulnerability")
            print(f"[03] Live GPS Tracker      [09] Leak & API Hunter")
            print(f"[04] Network Auditor       [10] System Utilities")
            print(f"[05] Payload Generator     [11] Image/Forensic Mechanic")
            print(f"[06] Bomber/Spammer        [12] Subdomain Sniper")
            print(f"[13] Cloudflare Bypass     [14] Google Dorking")
            print(f"[15] Generate PDF Report   [16] Global Phone Tracker")
            print(f"[00] Exit System{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.WHITE}mandesh@hacker ~# {Style.RESET_ALL}").strip()

            # Mapping choices to the specific Python script files
            commands = {
                "01": "mandesh_phish.py", "02": "mandesh_pi.py", 
                "03": "mandesh_hunt.py",  "04": "mandesh_audit.py", 
                "05": "mandesh_payload.py", "06": "mandesh_bomber.py",
                "07": "mandesh_crack.py", "08": "mandesh_webscan.py",
                "09": "mandesh_leak.py", "10": "mandesh_sys.py",
                "11": "mandesh_exif.py", "12": "mandesh_sniper.py",
                "13": "mandesh_cf_bypass.py", "14": "mandesh_google_dorking.py",
                "15": "mandesh_report.py", "16": "mandesh_track.py"
            }

            if choice == "00" or choice == "0": 
                print(f"{Fore.YELLOW}Shutting down Mandesh Suite...{Style.RESET_ALL}")
                break
                
            elif choice in commands or choice.zfill(2) in commands:
                cmd_key = choice if choice in commands else choice.zfill(2)
                # Execute the script
                os.system(f"python3 {commands[cmd_key]}")
                print(f"\n{Fore.YELLOW}>>> Task Complete. Press ENTER to return to menu...{Style.RESET_ALL}")
                input()
            else:
                print(f"{Fore.RED}Invalid option! Try again.{Style.RESET_ALL}")
                os.system("sleep 1")

if __name__ == "__main__":
    app = MandeshGUI()
    if app.authenticate(): 
        app.menu()
    else:
        print(f"{Fore.RED}Authentication Failed!{Style.RESET_ALL}")
