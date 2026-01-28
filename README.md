# Python-File-Integrity-Manager
A lightweight Host-Based Intrusion System (HIDS) built in Python. This tool provides real time monitoring of any directory, alerting users to unauthorized file modifications, deletions, and creations.


**WHY I BUILT THIS**
File integrity is a core component of cybersecurity and "Blue Team" defense. I built this tool to understand the underlying mechanics of enterprise solutions like Tripwire use to detect anomolies. This demonstrates pratical application of cryptographic hashing and automated incident response. 


**KEY FEATURES**
Real-Time Detection: Continuously polls a target directory for changes.

SHA-256 Hashing: Uses secure cryptographic hashing to create a "Golden Image" (baseline) of files.

GUI Dashboard: User-friendly interface built with Tkinter to view live logs and control the monitor.

Windows Integration: Sends native Windows Toast Notifications (win10toast) for instant alerts.

Persistent Logging: Detailed audit logs are saved to a dedicated Log + Baseline directory for review.

Non-Blocking Performance: Uses Python threading to ensure the UI remains responsive while the scanner runs in the background.

**Technicals Used**
Language: Python 3.12
GUI: tkinter 
Hashing: hashlib (SHA-256)
Notifications: win10toast

**Dependencies Needed**
pip install win10toast (This is used for creating the notifications)


**IMPORTANT DISCLAIMER**
This project was originally written for Command Line Interface (CLI) usage, and in doing so the CLI code was tested with a hard-coded directory and logfile + Baseline file storage, as for the GUI version, the save directory is a hard-coded location. If you do take this projec,t please change this. I will continue to update this project and make the file selection more seamless. 
