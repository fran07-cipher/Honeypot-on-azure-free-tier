import re
import csv
import json
import socket
from urllib.request import urlopen

input_file = "honeypot.log"
output_file = "cleaned.txt"

# Regex to capture IP after "IP: "
ip_pattern = re.compile(r"IP:\s*([\d\.]+)")

seen_ips = set()
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        match = ip_pattern.search(line)
        if match:
            ip = match.group(1)
            if ip not in seen_ips:
                seen_ips.add(ip)
                outfile.write(line)

print(f"Duplicates removed. Cleaned file saved as {output_file}")



# Files
input_file = "cleaned.txt"
output_file = "ips_enriched.csv"

# Regex to capture timestamp + IP
line_pattern = re.compile(r"\[(.*?)\]\s+- IP:\s+([\d\.]+)")

def lookup_ip(ip):
    """Lookup IP details using ip-api.com (free, ~45 req/min)"""
    try:
        with urlopen(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,org,as,query") as response:
            data = json.load(response)
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "N/A"),
                    "region": data.get("regionName", "N/A"),
                    "city": data.get("city", "N/A"),
                    "asn": data.get("as", "N/A"),
                    "org": data.get("org", "N/A"),
                }
    except Exception:
        pass
    return {"country": "N/A", "region": "N/A", "city": "N/A", "asn": "N/A", "org": "N/A"}

def reverse_dns(ip):
    """Try to resolve reverse DNS name"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "N/A"

rows = []

with open(input_file, "r") as infile:
    for line in infile:
        match = line_pattern.search(line)
        if match:
            timestamp, ip = match.groups()
            geo = lookup_ip(ip)
            r_dns = reverse_dns(ip)
            rows.append([
                timestamp,
                ip,
                geo["country"],
                geo["region"],
                geo["city"],
                geo["asn"],
                geo["org"],
                r_dns
            ])

# Write to CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "IP", "Country", "Region", "City", "ASN", "Org/ISP", "ReverseDNS"])
    writer.writerows(rows)

print(f"Enrichment done! CSV saved as {output_file}")


