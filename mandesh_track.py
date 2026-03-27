
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from colorama import Fore, Style

# PASTE YOUR KEY HERE
API_KEY = "YOUR_OPENCAGE_KEY" 

def track_number(number):
    try:
        # 1. Basic Info Extraction
        parsed_num = phonenumbers.parse(number)
        location = geocoder.description_for_number(parsed_num, "en")
        service_provider = carrier.name_for_number(parsed_num, "en")
        
        print(f"\n{Fore.GREEN}[+] Origin: {location}")
        print(f"[+] ISP: {service_provider}{Style.RESET_ALL}")

        # 2. GPS Coordinate Lookup
        geocoder_api = OpenCageGeocode(API_KEY)
        results = geocoder_api.geocode(location)
        
        if results:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            map_link = f"https://www.google.com/maps?q={lat},{lng}"
            
            print(f"{Fore.YELLOW}[*] Approx Coordinates: {lat}, {lng}")
            print(f"[*] Live Map: {map_link}{Style.RESET_ALL}")
            
            # Save to Database for Option [15] PDF Report
            with open("mandesh_db/tracking_logs.txt", "a") as f:
                f.write(f"Num: {number} | Loc: {location} | Maps: {map_link}\n")
        else:
            print(f"{Fore.RED}[!] Could not resolve GPS coordinates.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    print(f"{Fore.CYAN}=== MANDESH PHONE TRACKER v1.2.2 ==={Style.RESET_ALL}")
    num = input("Enter Number (e.g., +2547...): ").strip()
    if num:
        track_number(num)
