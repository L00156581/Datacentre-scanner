"""
evidence.py
Implements Step 5 of the assessment tool algorithm.
Handles saving raw security scan data to disk as audit evidence.
"""

from pathlib import Path  # Imports the tool used to manage file paths safely on any operating system.

# Set the save location for assessment files.
OUTPUT_DIRECTORY = Path("outputs")

def save_result(host, scan_result):
    """
    Saves raw Nmap text telemetry to a dedicated audit file on disk.
    Creates a separate clean log file for every evaluated target system.
    """
    # If the scan results are empty, skip writing to avoid blank files.
    if not scan_result:
        return False

    try:
        # Create the evidence directory structure if it does not already exist.
        OUTPUT_DIRECTORY.mkdir(
            exist_ok=True
        )

        # Replace dots in the IP address so that the filename is clean and system safe.
        safe_host_string = str(host).replace(".", "_")
        filename = f"evidence_{safe_host_string}.log"

        # Join the folder path and file name into a unified file path.
        file_path = OUTPUT_DIRECTORY / filename

        # Write the entire scan result to disk using UTF-8 encoding.
        file_path.write_text(
            scan_result,
            encoding="utf-8"
        )
        
        return True

    except (OSError, IOError) as error:
        # Handle disk write errors (e.g., permission issues, disk full) without crashing.
        print(f"[-] Critical Error: Failed to write evidence file for {host}. Reason: {error}")
        return False
