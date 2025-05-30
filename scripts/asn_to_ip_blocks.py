import sys
import dns.resolver

def get_prefixes_for_asn(asn):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5

    query = f'AS{asn}.asn.cymru.com'
    try:
        answers = resolver.resolve(query, 'TXT')
        prefixes = []
        for rdata in answers:
            decoded = rdata.to_text().strip('"')
            # Each record contains: ASN | IP Prefix | CC | RIR | Date
            parts = decoded.split('|')
            if len(parts) >= 2:
                prefix = parts[1].strip()
                prefixes.append(prefix)
        return prefixes
    except Exception as e:
        print(f"Lookup failed for ASN {asn}: {e}")
        return []

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
