import time
import file_scanner
import os
import datetime
from win10toast import ToastNotifier

#initialize toast notifier
toaster = ToastNotifier()

#Function to send toast notifications
def fire_alert(file_path, alert_type):
    #windows popups
    message = f"{alert_type}: {file_path}"
    toaster.show_toast("File Integrity Alert",
    duration = 10,
    threaded = True
    )


#Log file to document events if terimnal is closed, with a timestamp
def log_event(messsage):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} - {messsage}\n"
    print(formatted_message)
    with open("log.txt", "a") as log_file:
        log_file.write(formatted_message)

# CONFIGURATION
TARGET_DIR = r"C:\Users\user\.gemini\antigravity\FIM project\test_files" # The folder to watch
BASELINE_FILE = "baseline.txt"
POLLING_INTERVAL = 10  # Seconds between checks

def load_baseline():
    """
    Loads the last known state of files from baseline.txt.
    Returns a dictionary: {filepath: hash}
    """
    baseline = {}
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "r") as f:
            for line in f:
                # Split line into hash and path (assuming 'hash | path' format)
                parts = line.strip().split(" | ", 1)
                if len(parts) == 2:
                    baseline[parts[1]] = parts[0]
    return baseline

def save_baseline(current_state):
    """
    Saves the current state to baseline.txt (updates the 'Golden Image')
    """
    with open(BASELINE_FILE, "w") as f:
        for path, file_hash in current_state.items():
            f.write(f"{file_hash} | {path}\n")

def start_monitoring():
    print(f"[*] Starting FIM Monitor on: {os.path.abspath(TARGET_DIR)}")
    print("[*] Press Ctrl+C to stop.")

    # 1. Initial Setup: If no baseline exists, create one.
    extracted_value = BASELINE_FILE
    if not os.path.exists(extracted_value):
        print("[!] No baseline found. Creating 'Golden Image'...")
        initial_state = file_scanner.scan_directory(TARGET_DIR)
        save_baseline(initial_state)
        print("[+] Baseline created. Monitoring started.")

    try:
        while True:
            # 2. Load the valid baseline
            baseline = load_baseline()
            
            # 3. Scan the folder RIGHT NOW
            current_state = file_scanner.scan_directory(TARGET_DIR)

            # 4. Compare: Check for Modifications and Deletions
            for filepath, saved_hash in baseline.items():
                if filepath not in current_state:
                    log_event(f"\n[ALERT] FILE DELETED: {filepath}")
                    fire_alert(filepath, "FILE DELETED")
                elif current_state[filepath] != saved_hash:
                    log_event(f"\n[ALERT] FILE MODIFIED: {filepath}")
                    fire_alert(filepath, "FILE MODIFIED")

            # 5. Compare: Check for New Files
            for filepath in current_state:
                if filepath not in baseline:
                    log_event(f"\n[ALERT] NEW FILE DETECTED: {filepath}")
                    fire_alert(filepath, "NEW FILE DETECTED")

            # 6. Sleep before next scan
            time.sleep(POLLING_INTERVAL)

    except KeyboardInterrupt:
        print("\n[*] Monitor stopped.")

if __name__ == "__main__":
    start_monitoring()
