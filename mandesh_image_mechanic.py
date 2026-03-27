import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
from colorama import Fore, Style

class ImageMechanic:
    def __init__(self):
        self.db_path = "mandesh_db/forensics"
        os.makedirs(self.db_path, exist_ok=True)
        self.signatures = {"jpg": "ffd8ff", "png": "89504e47", "pdf": "25504446"}

    def get_exif(self, image_path):
        print(f"{Fore.CYAN}[*] Extracting Metadata: {image_path}{Style.RESET_ALL}")
        try:
            img = Image.open(image_path)
            info = img._getexif()
            if info:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    print(f"{Fore.GREEN}{decoded}: {value}")
            else: print(f"{Fore.YELLOW}[!] No EXIF data found.")
        except Exception as e: print(f"{Fore.RED}[-] Error: {e}")

    def deep_carve(self, device):
        print(f"{Fore.MAGENTA}[*] Initializing Deep Carve on {device}...{Style.RESET_ALL}")
        if os.getuid() != 0:
            print(f"{Fore.RED}[!] Error: Run with 'sudo' for disk access."); return
        
        output = os.path.join(self.db_path, f"carved_{os.path.basename(device)}")
        os.makedirs(output, exist_ok=True)
        
        try:
            with open(device, "rb") as disk:
                count = 0
                while True:
                    chunk = disk.read(512)
                    if not chunk: break
                    for ext, sig in self.signatures.items():
                        if chunk.startswith(bytes.fromhex(sig)):
                            count += 1
                            with open(f"{output}/rec_{count}.{ext}", "wb") as f:
                                f.write(chunk + disk.read(1024 * 1024))
                            print(f"{Fore.GREEN}[+] Carved: rec_{count}.{ext}")
                print(f"{Fore.YELLOW}[!] Success: {count} files recovered.")
        except Exception as e: print(f"{Fore.RED}[-] Error: {e}")

def main():
    mech = ImageMechanic()
    print(f"{Fore.CYAN}=== [11] IMAGE MECHANIC & FORENSICS ==={Style.RESET_ALL}")
    print("[1] EXIF Metadata Analysis (Local File)\n[2] Deep Forensic Carving (Raw Device)")
    
    choice = input("\nSelect Mode: ")
    if choice == '1':
        path = input("Enter Image Path: ")
        mech.get_exif(path)
    elif choice == '2':
        os.system("lsblk -p")
        dev = input("\nEnter Device (e.g., /dev/sdb1): ")
        mech.deep_carve(dev)

if __name__ == "__main__":
    main()
