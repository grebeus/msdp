import argparse
import re

parser = argparse.ArgumentParser(description='Finds 10 most commonipaddresses in log')
parser.add_argument("log_name", help="Path to the log file")
args = parser.parse_args()

ips = {}
with open(args.log_name) as file:
    pattern = r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
    for line in file: 
        for ip in re.findall(pattern, line):
            ips[ip] = ips.get(ip, 0) + 1

for top_ip in sorted(ips, key=ips.get, reverse=True)[:10]:
    print(top_ip, ips[top_ip])
