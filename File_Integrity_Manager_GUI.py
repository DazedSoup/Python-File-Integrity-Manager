import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import time
import os
import datetime
import file_scanner  # existing module
from win10toast import ToastNotifier

class FIMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FIM - File Integrity Monitor")
        self.root.geometry("700x550")
        
        # --- CONFIGURATION ---
        self.is_running = False
        self.target_dir = ""
        
        # 1. HARDCODED LOG PATH 
        # We use r"" (raw string) to handle the backslashes correctly
        self.log_dir = r"C:\Users\user\.gemini\antigravity\FIM project\Log + Baseline"
        
        # 2. AUTO-CREATE FOLDER
        # If this specific folder doesn't exist, we make it.
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir)
                print(f"Created log directory: {self.log_dir}")
            except OSError as e:
                messagebox.showerror("Error", f"Could not create log folder:\n{e}")
        
        # 3. SET FILE PATHS
        self.baseline_file = os.path.join(self.log_dir, "baseline.txt")
        self.log_file = os.path.join(self.log_dir, "fim_log.txt")
        
        # Initialize Notification System
        self.toaster = ToastNotifier()

        # --- UI LAYOUT ---
        tk.Label(root, text="File Integrity Monitor", font=("Arial", 16, "bold")).pack(pady=10)

        # Folder Selection
        frame_top = tk.Frame(root)
        frame_top.pack(pady=5)
        
        self.lbl_path = tk.Label(frame_top, text="No folder selected", fg="gray")
        self.lbl_path.pack(side=tk.LEFT, padx=10)
        
        btn_browse = tk.Button(frame_top, text="Select Folder", command=self.browse_folder)
        btn_browse.pack(side=tk.LEFT)

        # Control Buttons
        frame_controls = tk.Frame(root)
        frame_controls.pack(pady=10)
        
        self.btn_start = tk.Button(frame_controls, text="START MONITOR", bg="green", fg="white", 
                                   font=("Arial", 10, "bold"), command=self.start_monitoring)
        self.btn_start.pack(side=tk.LEFT, padx=10)
        
        self.btn_stop = tk.Button(frame_controls, text="STOP", bg="red", fg="white", 
                                  font=("Arial", 10, "bold"), command=self.stop_monitoring, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=10)

        # Log Area
        tk.Label(root, text="Live Activity Log:", font=("Arial", 10)).pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')
        self.log_area.pack(padx=10, pady=5)
        
        # Show user where files are saving
        tk.Label(root, text=f"The Log and Baseline are saved to: {self.log_dir}", fg="black", font=("Arial", 10)).pack(pady=5)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.target_dir = folder
            self.lbl_path.config(text=folder, fg="black")
            self.log_msg(f"Target set to: {folder}")

    def log_msg(self, message):
        """Updates the GUI AND writes to the text file."""
        # Update GUI
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"
        
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, formatted + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        
        # Write to File
        try:
            with open(self.log_file, "a") as f:
                f.write(formatted + "\n")
        except Exception as e:
            print(f"Error writing log: {e}")

    def fire_alert(self, filepath, alert_type):
        """Triggers the Windows Notification."""
        try:
            self.toaster.show_toast(
                "FIM Security Alert",
                f"{alert_type}: {os.path.basename(filepath)}",
                duration=3,
                threaded=True
            )
        except Exception as e:
            self.log_msg(f"Error showing notification: {e}")

    def start_monitoring(self):
        if not self.target_dir:
            messagebox.showwarning("Error", "Please select a folder first!")
            return

        self.is_running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.log_msg("[-] Sentry Mode Activated...")
        
        self.monitor_thread = threading.Thread(target=self.run_monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.is_running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.log_msg("[-] Monitoring Stopped.")

    def run_monitor_loop(self):
        self.log_msg("[-] Scanning baseline...")
        baseline = file_scanner.scan_directory(self.target_dir)
        
        # SAVE BASELINE TO THE SPECIFIC FOLDER
        try:
            with open(self.baseline_file, "w") as f:
                for path, h in baseline.items():
                    f.write(f"{h} | {path}\n")
            self.log_msg(f"[-] Baseline saved.")
        except Exception as e:
            self.log_msg(f"[!] Error saving baseline: {e}")
        
        while self.is_running:
            time.sleep(3)
            
            current_state = file_scanner.scan_directory(self.target_dir)
            
            # Check Modifications & Deletions
            for filepath, file_hash in baseline.items():
                if filepath not in current_state:
                    self.log_msg(f"ALERT: File DELETED -> {filepath}")
                    self.fire_alert(filepath, "FILE DELETED")
                    
                elif current_state[filepath] != file_hash:
                    self.log_msg(f"ALERT: File MODIFIED -> {filepath}")
                    self.fire_alert(filepath, "FILE MODIFIED")
            
            # Check New Files
            for filepath in current_state:
                if filepath not in baseline:
                    self.log_msg(f"ALERT: New File CREATED -> {filepath}")
                    self.fire_alert(filepath, "NEW FILE DETECTED")

if __name__ == "__main__":
    root = tk.Tk()
    app = FIMApp(root)
    root.mainloop()
