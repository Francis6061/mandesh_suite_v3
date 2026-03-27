import requests
from bs4 import BeautifulSoup
import webbrowser

def social_dorker(target):
    print(f"\n[*] Generating Social Footprint for: {target}")
    
    # List of platforms to pivot on
    platforms = [
        "facebook.com", 
        "twitter.com", 
        "linkedin.com", 
        "instagram.com", 
        "github.com"
    ]
    
    for site in platforms:
        # Construct the Dork URL
        query = f"https://www.google.com/search?q=site:{site} '{target}'"
        print(f"[+] {site.capitalize()}: {query}")
        
        # Optional: Uncomment the line below to open all links in your browser automatically
        # webbrowser.open(query)

# Example: social_dorker("francis6061") or social_dorker("email@example.com")

def scrape_profile(platform, username):
    urls = {
        "instagram": f"https://www.instagram.com/{username}/",
        "tiktok": f"https://www.tiktok.com/@{username}"
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(urls[platform], headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Searching for meta description (often contains the bio)
        meta_desc = soup.find("meta", property="og:description")
        return meta_desc['content'] if meta_desc else "Bio not found."
    except Exception as e:
        return f"Error: {str(e)}"

# Example Usage: print(scrape_profile("instagram", "francis6061"))
