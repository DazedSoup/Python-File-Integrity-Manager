# Python-File-Integrity-Manager
  A lightweight Host-Based Intrusion System (HIDS) built in Python. This tool provides real time monitoring of any directory, alerting users to unauthorized file modifications, deletions, and creations.
  
  
  
  
  
🛡️  
**WHY I BUILT THIS:**
  File integrity is a core component of cybersecurity and "Blue Team" defense. I built this tool to understand the underlying mechanics of enterprise solutions like Tripwire use to detect anomalies. This demonstrates the     practical application of cryptographic hashing and automated incident response. 
  
  
  
  
  
 🚀
  
**KEY FEATURES:**

  Real-Time Detection: Continuously polls a target directory for changes.

  SHA-256 Hashing: Uses secure cryptographic hashing to create a "Golden Image" (baseline) of files.

  GUI Dashboard: User-friendly interface built with Tkinter to view live logs and control the monitor.

  Windows Integration: Sends native Windows Toast Notifications (win10toast) for instant alerts.

  Persistent Logging: Detailed audit logs are saved to a dedicated Log + Baseline directory for review.

  Non-Blocking Performance: Uses Python threading to ensure the UI remains responsive while the scanner runs in the background.
  
   
  
  
  
  🛠️
  
**Technicals Used:**

  Language: Python 3.12
  
  GUI: tkinter 
  
  Hashing: hashlib (SHA-256)
  
  Notifications: win10toast

  
  
  
  
  
  
  
  
  
**Dependencies Needed:**
  pip install win10toast (This is used for creating the notifications)
  

📂

**Project Structure:**

fim_gui.py - The main entry point. Handles the UI, threading, and alerting logic.

file_scanner.py - The engine. Handles file iteration and SHA-256 calculation.

baseline.txt - Stores the cryptographic fingerprint of the target directory.

fim_log.txt - Time-stamped audit log of all detected events.

🔮





  **Future Roadmap:**
  
  Migrate from text-based logs to SQLite for better query performance.
  
  Add Discord Webhook integration for remote monitoring.
  
  Allow users to set the scan interval instead of a predetermined interval.
  

  🖥️
  
**IMPORTANT DISCLAIMER:**
  This project was originally written for Command Line Interface (CLI) usage, and in doing so the CLI code was tested with a hard-coded directory and logfile + Baseline file storage. For the GUI version, the save directory for the baseline and log is also a hard-coded location. If you do take this project, please change this. I will continue to update this project and make the file selection more seamless. 



🚀


  **Some images of running the GUI**

  <img width="690" height="567" alt="FIM ss1" src="https://github.com/user-attachments/assets/ee4eda27-8f53-4079-b792-454e9db85537" />


  <img width="1444" height="462" alt="FIM ss2" src="https://github.com/user-attachments/assets/37cbadba-7557-4cfb-81e6-161bda4001ca" />


  <img width="756" height="690" alt="FIM ss3" src="https://github.com/user-attachments/assets/100ba424-6bba-4ba4-a5a9-f3bf2a03342f" />


  <img width="992" height="599" alt="FIM ss4" src="https://github.com/user-attachments/assets/9872b6ff-d638-42d8-8cea-6b7822306104" />
  









  
