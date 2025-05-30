import sys
import requests
import os

def get_prefixes_for_asn(asn):
    url = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{asn}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data for ASN {asn}: {response.status_code}")
        return []
    data = response.json()
    prefixes = [item['prefix'] for item in data['data']['prefixes']]
    return prefixes

def read_existing_prefixes(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def write_updated_prefixes(prefixes, file_path):
    with open(file_path, 'w') as f:
        for prefix in sorted(prefixes):
            f.write(prefix + '\n')
    print(f"Updated {file_path} with {len(prefixes)} unique prefixes")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python asn_to_ip_blocks.py <ASN>")
        sys.exit(1)
    asn = sys.argv[1]
    file_path = 'asn_block1.1.txt'

    # Get new prefixes
    new_prefixes = set(get_prefixes_for_asn(asn))
    if not new_prefixes:
        print(f"No prefixes found for ASN {asn}")
        sys.exit(0)

    # Read existing prefixes
    existing_prefixes = read_existing_prefixes(file_path)

    # Merge and deduplicate
    all_prefixes = existing_prefixes.union(new_prefixes)

    # Write updated list
    write_updated_prefixes(all_prefixes, file_path)
