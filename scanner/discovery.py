"""
discovery.py
Implements Step 2 of the assessment tool algorithm
Handles multi threaded host discovery using parallel ICMP ping sweeps.
Works on both Linux and Windows.
"""

import subprocess # Imports the module used to run system commands (like ping).
import concurrent.futures # Manages pools of asynchronous worker threads for speed.
import platform  # Dynamic OS detection engine.

def ping_host(ip):
    """
    Tests a single IP address using an ICMP network ping.
    Adapts parameters depending on the host Operating System.
    """
    # Detect the current operating system platform.
    current_os = platform.system().lower()

    if current_os == "windows":
        # Windows ping configurations -
        # -n 1 = Send exactly 1 packet.
        # -w 1000 = Wait up to 1000 milliseconds (1 second).
        command = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        # Linux/macOS ping configurations -
        # -c 1 = Send exactly 1 packet.
        # -W 1 = Wait up to 1 second.
        command = ["ping", "-c", "1", "-W", "1", str(ip)]

    # Execute the OS-appropriate ping command.
    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL, # Mutes the standard terminal text output from the ping command.
        stderr=subprocess.DEVNULL  # Mutes any error messages thrown by the ping command.
    )

    # Both operating systems return 0 when a ping succeeds.
    if result.returncode == 0:
        return str(ip)

    return None

def discover_hosts(network, threads=20):
    """
    Sweeps an entire network range concurrently to locate live hosts.
    """
    live_hosts = []

    # Extract all usable host IP addresses from the network object.
    addresses = list(network.hosts())

    # Initialise a pool of reusable background threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        
        # Asynchronously assign the ping_host function to each IP address.
        results = executor.map(ping_host, addresses)

        # Collect and filter the results.
        for result in results:
            if result:
                live_hosts.append(result)

    return live_hosts