
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from urllib.parse import urljoin

class MandeshScanner:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        # Common payloads for automation
        self.xss_payload = "<script>alert('XSS')</script>"
        self.sqli_payload = "' OR '1'='1"

    def get_forms(self, url):
        soup = BeautifulSoup(self.session.get(url).content, "html.parser")
        return soup.find_all("form")

    def scan_xss(self, url):
        print(f"{Fore.CYAN}[*] Testing XSS on: {url}{Style.RESET_ALL}")
        forms = self.get_forms(url)
        for form in forms:
            action = form.get("action")
            post_url = urljoin(url, action)
            method = form.get("method", "get").lower()
            
            data = {}
            for input_tag in form.find_all("input"):
                name = input_tag.get("name")
                type = input_tag.get("type", "text")
                if type == "text" or type == "search":
                    data[name] = self.xss_payload
            
            if method == "post":
                res = self.session.post(post_url, data=data)
            else:
                res = self.session.get(post_url, params=data)
                
            if self.xss_payload in res.text:
                print(f" {Fore.RED}[!] VULNERABILITY FOUND: XSS")
                print(f"  [>] Location: {post_url}")
                print(f"  [>] Type: Reflected XSS via Form Input{Style.RESET_ALL}")

    def scan_sqli(self, url):
        print(f"{Fore.CYAN}[*] Testing SQLi on URL parameters...{Style.RESET_ALL}")
        test_url = f"{url}?id={self.sqli_payload}"
        res = self.session.get(test_url)
        # Check for common SQL error strings
        errors = ["mysql_fetch_array()", "PostgreSQL query failed", "SQL syntax;"]
        for error in errors:
            if error in res.text:
                print(f" {Fore.RED}[!] VULNERABILITY FOUND: SQL Injection")
                print(f"  [>] Location: {test_url}")
                print(f"  [>] Type: Error-based SQLi{Style.RESET_ALL}")

    def run(self):
        print(f"{Fore.RED}=== MANDESH VULNERABILITY SCANNER ==={Style.RESET_ALL}")
        self.scan_xss(self.target)
        self.scan_sqli(self.target)

if __name__ == "__main__":
    target_url = input("Enter Target URL (e.g., http://testphp.vulnweb.com/): ")
    scanner = MandeshScanner(target_url)
    scanner.run()







#########
'''import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

class MandeshWebScan:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.xss_payloads = ["<script>alert('XSS')</script>", "';alert(1)//", "<img src=x onerror=alert(1)>"]

    def get_all_forms(self):
        # Extract all forms to test for injection points
        soup = BeautifulSoup(self.session.get(self.url).content, "html.parser")
        return soup.find_all("form")

    def test_xss(self):
        print(f"{Fore.CYAN}[*] Scanning for XSS vulnerabilities...{Style.RESET_ALL}")
        forms = self.get_all_forms()
        print(f"[!] Found {len(forms)} forms on page.")
        
        for form in forms:
            details = self.get_form_details(form)
            for payload in self.xss_payloads:
                res = self.submit_form(details, payload)
                if payload in res.text:
                    print(f"{Fore.GREEN}[+] XSS Detected in form at {self.url}{Style.RESET_ALL}")
                    print(f"  [>] Payload: {payload}")
                    break

    def get_form_details(self, form):
        details = {}
        action = form.attrs.get("action", "").lower()
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            inputs.append({"type": input_tag.attrs.get("type", "text"), "name": input_tag.attrs.get("name")})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    def submit_form(self, form_details, value):
        target_url = self.url + form_details["action"]
        data = {}
        for input in form_details["inputs"]:
            if input["type"] == "text" or input["type"] == "search":
                data[input["name"]] = value
            else:
                data[input["name"]] = "test"
        if form_details["method"] == "post":
            return self.session.post(target_url, data=data)
        return self.session.get(target_url, params=data)

if __name__ == "__main__":
    target = input("Enter URL to scan (e.g., http://example.com/): ")
    scanner = MandeshWebScan(target)
    scanner.test_xss()
'''
