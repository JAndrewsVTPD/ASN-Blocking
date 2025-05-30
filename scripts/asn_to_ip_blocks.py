import sys
import requests

def get_ip_blocks(asn):
    url = f"https://api.bgpview.io/asn/{asn}/prefixes"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for ASN {asn}: {response.status_code}")
        return []
    data = response.json()
    prefixes = []
    for prefix in data.get('data', {}).get('ipv4_prefixes', []) + data.get('data', {}).get('ipv6_prefixes', []):
        prefixes.append(prefix.get('prefix'))
    return prefixes

def write_to_file(prefixes, filename):
    with open(filename, 'w') as f:
        for prefix in prefixes:
            f.write(prefix + '\n')
    print(f"Written {len(prefixes)} prefixes to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python asn_to_ip_blocks.py <ASN>")
        sys.exit(1)
    asn = sys.argv[1]
    prefixes = get_ip_blocks(asn)
    if prefixes:
        write_to_file(prefixes, f"asn_{asn}_blocks.txt")

