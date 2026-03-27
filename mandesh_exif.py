
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from colorama import Fore, Style

def get_exif(image_path):
    print(f"{Fore.CYAN}[*] Analyzing: {image_path}{Style.RESET_ALL}")
    try:
        image = Image.open(image_path)
        info = image._getexif()
        if not info:
            print(f"{Fore.RED}[!] No EXIF metadata found.{Style.RESET_ALL}")
            return

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                print(f"{Fore.GREEN}[+] GPS DATA FOUND!{Style.RESET_ALL}")
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    print(f"  {sub_tag}: {value[t]}")
            else:
                print(f" {decoded}: {value}")
                
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

def mechanic_main():
    print(f"{Fore.MAGENTA}=== MANDESH IMAGE MECHANIC (EXIF) ==={Style.RESET_ALL}")
    img_path = input("Enter path to image (e.g., target.jpg): ")
    if os.path.exists(img_path):
        get_exif(img_path)
    else:
        print(f"{Fore.RED}[!] File not found.{Style.RESET_ALL}")

if __name__ == "__main__":
    mechanic_main()




'''from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    image = Image.open(image_path)
    info = image._getexif()
    if not info:
        return "No metadata found."
    
    exif_table = {}
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif_table[decoded] = value
    return exif_table

# Logic to extract GPS specifically
def get_gps_info(exif_data):
    gps_info = exif_data.get("GPSInfo")
    if not gps_info:
        return "No GPS data."
    return gps_info


def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def get_maps_link(gps_info):
    try:
        lat = convert_to_degrees(gps_info[2])
        if gps_info[1] != 'N': lat = 0 - lat
        
        lon = convert_to_degrees(gps_info[4])
        if gps_info[3] != 'E': lon = 0 - lon
        
        return f"https://www.google.com/maps?q={lat},{lon}"
    except:
        return "Invalid GPS Format"
'''
