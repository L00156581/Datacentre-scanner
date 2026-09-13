"""
main.py

Main controller for the algorithmic datacentre security testing tool.
"""

import sys # Used for system operations, standard error flags, and exit codes.
import argparse # Handles command-line arguments.

# Import the individual components of the assessment algorithm.
from scanner.validator import validate_subnet
from scanner.discovery import discover_hosts
from scanner.nmap_scanner import scan_host
from scanner.database_check import check_database_service
from scanner.evidence import save_result

def main():
    # Create command-line interface.
    parser = argparse.ArgumentParser(
        description="Algorithmic Data Centre Security Assessment"
    )

    # Require the tester to specify the authorised network.
    parser.add_argument(
        "subnet",
        help="Authorised laboratory network in CIDR notation"
    )

    # Allow the number of concurrent discovery threads to be changed.
    # Optional to adjust speed/performance.
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=20,
        help="Number of concurrent discovery workers"
    )

    # Read the command-line arguments & parse into variables.
    args = parser.parse_args()

    # 1. SCOPE VALIDATION
    # Verify target is inside authorised scope.
    subnet = validate_subnet(args.subnet)
    print(f"[*] Assessment scope: {subnet}")

    # 2. HOST DISCOVERY
    # The discovery module checks addresses in the authorised network and returns the hosts that respond.
    hosts = discover_hosts(subnet, args.threads)

    # Stop the assessment if no hosts were discovered.
    if not hosts:
        print("[-] No live hosts discovered.")
        sys.exit(0)

    print(f"[+] {len(hosts)} live hosts discovered.")

    # 3. SERVICE DISCOVERY
    # Loop through each active target located.
    # Each discovered host is passed to the Nmap module.
    # Nmap identifies open ports and available services.
    for host in hosts:
        print(f"[*] Assessing {host}")
        result = scan_host(host)
    
        # Save the Nmap results as evidence.
        save_result(host, result)

        # 4. CONDITIONAL DATABASE ASSESSMENT
        # The algorithm examines the Nmap results.
        # If database signatures (TCP/3306, TCP/5432, TCP/1433) are open,
        # the database assessment condition is activated.
        # Otherwise the program continues to the next host.    
        if check_database_service(result):
            print(f"[!] Database service detected on {host}")

    # Assessment completed.
    print("[+] Assessment complete.")

# Run main() only when this file is executed directly.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Assessment cancelled by user.")
        sys.exit(1)
