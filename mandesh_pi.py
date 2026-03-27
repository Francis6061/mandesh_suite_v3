import phonenumbers
from phonenumbers import geocoder, carrier
from colorama import Fore, Style
import mandesh_breach, mandesh_social, mandesh_pivot # Your sub-modules

def phone_info(number):
    try:
        # Standardize for Kenyan numbers if + is missing
        if number.startswith('0'):
            number = "+254" + number[1:]
            
        parsed = phonenumbers.parse(number)
        location = geocoder.description_for_number(parsed, "en")
        service = carrier.name_for_number(parsed, "en")
        
        print(f"\n{Fore.GREEN}[+] Region: {location}")
        print(f"[+] Carrier: {service}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error parsing number: {e}{Style.RESET_ALL}")

def intelligence_hub():
    print(f"{Fore.MAGENTA}=== MANDESH IDENTITY INTELLIGENCE HUB ==={Style.RESET_ALL}")
    inp = input("Enter Target (Email/Phone/Username): ").strip()
    
    # Logic 1: Phone Numbers (e.g., +254712... or 0712...)
    if inp.startswith("+") or (inp.isdigit() and len(inp) >= 10):
        print(f"{Fore.YELLOW}[*] Detecting Phone Number...{Style.RESET_ALL}")
        phone_info(inp)
    
    # Logic 2: Emails
    elif "@" in inp:
        print(f"{Fore.YELLOW}[*] Detecting Email...{Style.RESET_ALL}")
        mandesh_breach.check_breach(inp)
        mandesh_social.social_dorker(inp)
        mandesh_pivot.check_recovery(inp)
        
    # Logic 3: Usernames
    else:
        print(f"{Fore.YELLOW}[*] Detecting Username...{Style.RESET_ALL}")
        mandesh_social.social_dorker(inp)
        mandesh_breach.check_breach(inp)

if __name__ == "__main__":
    intelligence_hub()
