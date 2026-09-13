"""
validator.py
Implements Step 1 of the assessment tool algorithm
Validates the network range to ensure it stays within authorised limits.
"""

import ipaddress

def validate_subnet(subnet):
    # Validates a CIDR network string and enforces lab scope safety.
    try:
        # Convert input string into a network object
        # strict=False safely handles host bits (e.g., .15/24) without crashing
        network = ipaddress.ip_network(subnet, strict=False)

    except ValueError as error:
        # Catch and reject invalid network formats
        raise ValueError("Invalid CIDR network format.") from error

    # Enforce strict laboratory boundaries
    authorised_network = ipaddress.ip_network("192.168.10.0/24")

    # Safety - Block execution if target falls outside the lab scope
    if not network.subnet_of(authorised_network):
        raise ValueError(
            "Target network is outside the authorised laboratory scope."
        )

    return network
