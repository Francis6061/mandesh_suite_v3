import webbrowser
from colorama import Fore, Style

def dorking_main():
    print(f"{Fore.BLUE}=== MANDESH DORKING MASTER [14] ==={Style.RESET_ALL}")
    target = input("Enter Target Domain (e.g., example.com): ")
    
    dorks = {
        "1": f"site:{target} filetype:pdf",
        "2": f"site:{target} filetype:env OR filetype:sql",
        "3": f"site:{target} inurl:admin OR inurl:login",
        "4": f"site:{target} intitle:\"index of\""
    }
    
    print("\n[1] Find PDFs  [2] Find Configs/DBs  [3] Find Admin Panels  [4] Directory Listing")
    choice = input("\nSelect Dork Type: ")
    
    if choice in dorks:
        query = dorks[choice].replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        print(f"{Fore.GREEN}[*] Opening Search: {url}{Style.RESET_ALL}")
        # Note: This might require a GUI browser on Chromebook
        print(f"Copy/Paste this to your browser: {url}")
    else:
        print("Invalid Choice.")

if __name__ == "__main__":
    dorking_main()
