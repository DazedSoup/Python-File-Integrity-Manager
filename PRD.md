
**Python File Integrity Monitor (FIM) Version: 1.0  Author: 
<br>
[Tarun Satish]**
<br>
<br>
<br>
**1. Problem Statement**

In cybersecurity defense (Blue Team operations), unauthorized changes to system files are often the first indicator of a compromise. Malware, ransomware, and attackers often modify configuration files or inject new executables. Manual verification of thousands of files is impossible for human administrators.
<br>
<br>
<br>
**2. Solution Overview**

The FIM is a host-based security tool that automates the detection of file anomalies. It establishes a cryptographic "Golden Image" (baseline) of a target directory and continuously monitors for deviations (modifications, deletions, creations), alerting the user in real-time
<br>
<br>
<br>
**3. Key Objectives**

Integrity Verification: Use industry-standard hashing (SHA-256) to ensure file authenticity.

Real-Time Response: Minimize the time between a file change and user notification (Target: < 5 seconds).

Usability: Provide a Graphical User Interface (GUI) so non-technical users can operate the tool without command-line knowledge.

Forensics: Maintain a permanent audit log of all events for post-incident analysis.
<br>
<br>
<br>

**4. Functional Requirements**

  4.1 Scanning Engine

    FR.1.1: The system must utilize the SHA-256 hashing algorithm via Python's hashlib.

    FR.1.2: The system must ignore the specific folder where logs are stored to prevent infinite loops.

  4.2 Monitoring Logic
  
    FR.2.1: The system must detect File Modifications (Hash mismatch).

    FR.2.2: The system must detect File Deletions (Path exists in baseline but not on disk).

    FR.2.3: The system must detect File Creations (Path exists on disk but not in baseline).

    FR.2.4: The polling interval shall be set to 3 seconds.

  4.3 User Interface (GUI)
  
    FR.3.1: The application shall be built using Tkinter.

    FR.3.2: The UI must display a scrolling log of live events.

    FR.3.3: The UI must remain responsive during scanning (implemented via threading).

  4.4 Alerting & Logging

    FR.4.1: Alerts must trigger a native Windows Toast Notification using win10toast.

    FR.4.2: All alerts must be appended to fim_log.txt with a [YYYY-MM-DD HH:MM:SS] timestamp.

    FR.4.3: Logs must be saved to a persistent user directory (.gemini/antigravity/...).
<br>
<br>
<br>

**5. Non-Functional Requirements**

Performance: The application should consume minimal CPU (< 5%) when monitoring small to medium directories (< 10,000 files).

Reliability: The application must handle file permission errors gracefully (e.g., skip locked files) without crashing.

Compatibility: Targeted for Windows 10/11 environments.
<br>
<br>
<br>
**6. Future Scope (V2.0)**
   
Integration with Cloud SIEM via API.

Discord/Slack Webhook integration for remote mobile alerts.

SQLite database implementation for historical trend analysis.

Recursive directory exclusion patterns (e.g., ignore .tmp files).
