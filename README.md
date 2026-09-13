# Algorithmic Data Centre Security Testing Framework & Lab Sandbox

[License: MIT](LICENSE.md)

[Python 3.13+](https://www.python.org/downloads/release/python-3137/)

This repository contains the official, open-source implementation presented in the project paper: **"Algorithmic Pen Test Procedure for a Data Centre and Report Structure"**. 

It consists of a two part framework for data centre cybersecurity testing:
1. **Infrastructure Implementation:** A PowerShell script (`Create-DatacentreLab.ps1`) that automatically implements a fully isolated, private Hyper-V simulation sandbox containing an attacker platform and three strategic target hosts.
2. **Algorithmic Security Assessment Tool:** A modular Python program 3hat automatically finds active computers on a network, checks what services they are running and safely logs security vulnerabilities.

---

## System Structure

```text

PHASE 1: INFRASTRUCTURE IMPLEMENTATION 

[Create-DatacentreLab.ps1] 
   └── Create Storage Paths ──> Build Private Virtual Switch ──> Deploy 4 Static VMs
 

PHASE 2: ALGORITHMIC ASSESSMENTS (Isolated Network)
 
[main.py Coordinator]                                                
   ├── 1. validator.py     <── Enforces scope boundary (192.168.10.0/24).
   ├── 2. discovery.py     <── Multi-thread ICMP sweep across active hosts.
   ├── 3. nmap_scanner.py  <── Scan to identify active software and versions running on a network.
   ├── 4. database_check.py<── Indicates high-value targets (Ports 3306, 5432, 1433).
   └── 5. evidence.py      <── Saves logs locally.
```

---

## Repository Layout

```text
datacentre_scanner/
│
├── Create-DatacentreLab.ps1   # Lab environment implementation script (PowerShell).
├── main.py                    # Main control to start the program (Python).
├── .gitignore                 # Excludes local test logs and python caches.
└── scanner/                   # Core scanning toolkit.
    ├── __init__.py            # File to indicate folder contains Python tool components.
    ├── validator.py           # Scope verification and safety boundaries.
    ├── discovery.py           # Fast, multi-threaded network host discovery.
    ├── nmap_scanner.py        # Deep port scanning and service identification.
    ├── database_check.py      # Exposure testing and vulnerability evaluation
    └── evidence.py            # Secure logger that safely saves findings to hard drive without crashing.
```

---

## Core Features

### 1. Automated Lab Provisioning (`PowerShell`)
* **Total Isolation:** Deploys a Private Hyper-V virtual switch with no internet leak.
* **Portable Directory Mapping:** Automatically builds the lab footprint wherever you clone the repo.
* **Pre-Configured Infrastructure:** Instantly builds an attacking machine node and three target servers.

### 2. Multi-Threaded Scanning Pipeline (`Python`)
* **Scope Guard:** The `validator.py` program blocks the scan and throws an error if the target is outside approved lab boundaries.
* **OS Adaptability:** The `discovery.py` module automatically adjusts ping commands depending on whether the tool is running on Windows or Linux.
* **Deep Service Fingerprinting:** Wraps Nmap to extract precise application software names, version and exposed database states.
* **Structured Evidence:** The `evidence.py` captures scan results and saves them in a localised `/outputs` folder using masked target naming schemes (`evidence_192_168_10_x.log`).


---

## Prerequisites & System Requirements

Before deploying the environment, ensure your host computer meets the following criteria:

* **Operating System:** Windows 10 or Windows 11 **Pro, Enterprise, or Education**.
* **Hardware:** Intel or AMD CPU with **Virtualization (VT-x/AMD-V) enabled** in the BIOS.
* **Dependencies:** Nmap must be installed on your host system if running the scanner locally.

---
## Setup & Execution Guide

### Phase 1: Environment Implementation (Windows Host)

1. Open a Windows PowerShell terminal window with **Administrative Privileges** (`Run as Administrator`).
2. Navigate to the cloned repository folder.
3. Drop OS installation files (`.iso`) into the newly mapped `ISO/` folder.
4. Execute the script to construct the sandboxed Hyper-V environment:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\Create-DatacentreLab.ps1
   ```
5. Ensure the target IPs inside the private network space are allocated within the authorised `192.168.10.0/24` subnet boundaries.

### Phase 2: Running the Security Assessment Tool

Log into your attacker system (`Assessment-VM`) connected to the `DC-Lab-Switch` private interface. Navigate to the project folder and run.

*Note: Administrative/root permissions are required by underlying network tools like Nmap.*

```bash
# Run the scanner with default settings (20 discovery threads)
sudo python3 main.py 192.168.10.0/24

# Alter performance by defining number of concurrent worker threads
sudo python3 main.py 192.168.10.0/24 --threads 50
```
All captured scan data and evidence logs are automatically masked and saved locally inside the `/outputs` folder (e.g., `evidence_192_168_10_x.log`).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for complete details.
