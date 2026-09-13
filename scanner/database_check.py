"""
database_check.py
Implements Step 4 of the assessment tool algorithm.
Parses raw Nmap scanner results to identify exposed database systems.
The function only identifies the service condition.
It does not automatically exploit the database.
"""

def check_database_service(scan_result):
    """
    Examines raw Nmap text output to identify signs of open database setting.
    Returns True if database indicators are found, otherwise returns False.
    """
    # Defensive execution check: Ensure the input payload contains actual string data.
    if not scan_result or not isinstance(scan_result, str):
        return False

    # Database network activity is identified by three standard ports
    # - 3306/tcp = MySQL / MariaDB default.
    # - 5432/tcp = PostgreSQL default.
    # - 1433/tcp = Microsoft SQL Server default.
    database_signatures = [
        "3306/tcp open",
        "5432/tcp open",
        "1433/tcp open",
        "mysql",
        "postgresql",
        "ms-sql"
    ]

    # Convert raw text to lowercase to ensure signature matching isn't affected by capitalisation variations.
    normalised_result = scan_result.lower()

    # Search the results for target database signatures.
    for signature in database_signatures:
        if signature in normalised_result:
            return True

    # No target database signatures detected.
    return False
