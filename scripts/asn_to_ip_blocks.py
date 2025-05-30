import sys
import requests

def get_prefixes_for_asn(asn):
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{asn}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for ASN {asn}: {response.status_code}")
        return []
    data = response.json()
    prefixes = [item['prefix'] for item in data['data']['prefixes']]
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
    prefixes = get_prefixes_for_asn(asn)
    if prefixes:
        write_to_file(prefixes, f"asn_{asn}_blocks.txt")
    else:
        print(f"No prefixes found for ASN {asn}")
