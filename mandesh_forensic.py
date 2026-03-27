import os
import json
import pytsk3
from colorama import Fore, Style

class MandeshForensic:
    def __init__(self):
        self.log_data = []
        self.sig_file = "mandesh_db/signatures.json"
        self.db_path = "mandesh_db/recovered_files"
        
        # Default Magic Byte Signatures (Hex)
        self.signatures = {
            "jpg": "ffd8ff",
            "png": "89504e47",
            "pdf": "25504446",
            "zip": "504b0304",
            "mp4": "0000001866747970",
            "exe": "4d5a"
        }
        self.load_signatures()

    def load_signatures(self):
        """Loads custom signatures from JSON and converts to bytes."""
        if os.path.exists(self.sig_file):
            try:
                with open(self.sig_file, "r") as f:
                    hex_dict = json.load(f)
                self.signatures.update(hex_dict)
                print(f"{Fore.GREEN}[+] Loaded {len(self.signatures)} signatures.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Signature JSON error: {e}{Style.RESET_ALL}")
        
        self.sig_bytes = {k: bytes.fromhex(v) for k, v in self.signatures.items()}

    def log(self, text, color=Fore.WHITE):
        print(f"{color}{text}{Style.RESET_ALL}")
        self.log_data.append(text)

    def recover_filesystem_files(self, device_path, output_dir):
        """Mode 1: Recover via File System metadata (Preserves names)."""
        self.log(f"[*] Scanning File System: {device_path}", Fore.CYAN)
        try:
            img = pytsk3.Img_Info(device_path)
            fs = pytsk3.FS_Info(img)
            root = fs.open_dir(path="/")
            
            count = 0
            for fs_object in root:
                if not fs_object.info.meta or fs_object.info.name.name in [b".", b".."]:
                    continue
                
                name = fs_object.info.name.name.decode('utf-8', errors='replace')
                is_deleted = fs_object.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC
                status = "DELETED" if is_deleted else "ACTIVE"
                
                self.log(f"  [{status}] {name}", Fore.GREEN if not is_deleted else Fore.YELLOW)
                
                # Read and save
                file_data = fs_object.read_random(0, fs_object.info.meta.size)
                with open(os.path.join(output_dir, name), "wb") as f:
                    f.write(file_data)
                count += 1
            return count
        except Exception as e:
            self.log(f"[-] FS Recovery skipped/failed: {e}", Fore.RED)
            return 0

    def deep_carve(self, device_path, output_dir):
        """Mode 2: Raw byte carving (For formatted/corrupt drives)."""
        self.log(f"[*] Starting Deep Carve (Raw Signature Scan)...", Fore.MAGENTA)
        file_count = 0
        try:
            with open(device_path, "rb") as disk:
                chunk_size = 512 # Sector size
                while True:
                    chunk = disk.read(chunk_size)
                    if not chunk: break
                    
                    for ext, sig in self.sig_bytes.items():
                        if chunk.startswith(sig):
                            file_count += 1
                            file_name = f"carved_{file_count}.{ext}"
                            self.log(f"  [+] Found {ext.upper()}! Carving...", Fore.GREEN)
                            
                            # Save chunk + 2MB buffer (basic carving logic)
                            with open(os.path.join(output_dir, file_name), "wb") as f:
                                f.write(chunk + disk.read(1024 * 2048)) 
            return file_count
        except Exception as e:
            self.log(f"[-] Deep Carve Error: {e}", Fore.RED)
            return 0

    def start(self, device_path):
        if os.getuid() != 0:
            self.log("[!] Error: Run with 'sudo' for raw disk access.", Fore.RED)
            return

        output_dir = os.path.join(self.db_path, f"recovery_{os.path.basename(device_path)}")
        os.makedirs(output_dir, exist_ok=True)

        fs_count = self.recover_filesystem_files(device_path, output_dir)
        dc_count = self.deep_carve(device_path, output_dir)

        self.log(f"\n[!] Task Finished.", Fore.YELLOW)
        self.log(f"    FS Recovered: {fs_count}")
        self.log(f"    Raw Carved: {dc_count}")
        self.log(f"    Results in: {output_dir}")

if __name__ == "__main__":
    forensic = MandeshForensic()
    print(f"{Fore.RED}=== MANDESH FORENSIC CARVER v1.2.2 ==={Style.RESET_ALL}")
    
    os.system("lsblk -p | grep -v 'loop'")
    target = input("\nEnter target device (e.g., /dev/sdb1): ").strip()
    
    if target:
        forensic.start(target)
