#!/usr/bin/env python3

import re
import subprocess
import sys
from pathlib import Path

CVE_REGEX = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)


def extract_cves(filename):
    text = Path(filename).read_text(errors="ignore")
    cves = {
        match.upper()
        for match in CVE_REGEX.findall(text)
    }
    return sorted(cves)


def search_cve(cve):
    command = [
        "msfconsole",
        "-q",
        "-x",
        f"search cve:{cve}; exit"
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    return result.stdout


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} cves.txt")
        sys.exit(1)

    filename = sys.argv[1]
    cves = extract_cves(filename)

    if not cves:
        print("No CVEs found.")
        return

    print(f"Found {len(cves)} unique CVEs.\n")

    for cve in cves:
        print("=" * 70)
        print(f"Searching Metasploit for {cve}")
        print("=" * 70)

        output = search_cve(cve)
        print(output)


if __name__ == "__main__":
    main()
