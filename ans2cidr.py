#!/usr/bin/env python3

import argparse
import ipaddress
import requests
import sys


RIPESTAT_URL = "https://stat.ripe.net/data/announced-prefixes/data.json"


def get_prefixes(asn):
    resource = f"AS{asn}"

    try:
        response = requests.get(
            RIPESTAT_URL,
            params={"resource": resource},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error querying RIPEstat: {e}", file=sys.stderr)
        sys.exit(1)

    data = response.json()

    return [
        item["prefix"]
        for item in data.get("data", {}).get("prefixes", [])
    ]


def filter_prefixes(prefixes, ipv4=False, ipv6=False):
    result = []

    for prefix in prefixes:
        try:
            network = ipaddress.ip_network(prefix)

            if ipv4 and isinstance(network, ipaddress.IPv4Network):
                result.append(prefix)

            elif ipv6 and isinstance(network, ipaddress.IPv6Network):
                result.append(prefix)

            elif not ipv4 and not ipv6:
                result.append(prefix)

        except ValueError:
            continue

    return sorted(result)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Get announced IP prefixes for an ASN using RIPEstat. "
            "Returns both IPv4 and IPv6 prefixes by default."
        )
    )

    parser.add_argument(
        "asn",
        nargs="?",
        type=int,
        help="ASN number (without AS prefix)"
    )

    parser.add_argument(
        "--asn",
        dest="asn_option",
        type=int,
        help="ASN number (alternative to the positional argument)"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--ipv4",
        "-4",
        action="store_true",
        help="Return only IPv4 prefixes"
    )

    group.add_argument(
        "--ipv6",
        "-6",
        action="store_true",
        help="Return only IPv6 prefixes"
    )

    args = parser.parse_args()

    if args.asn is not None and args.asn_option is not None:
        parser.error("provide the ASN either as a positional argument or with --asn, not both")

    asn = args.asn if args.asn is not None else args.asn_option
    if asn is None:
        parser.error("an ASN is required")

    prefixes = get_prefixes(asn)

    prefixes = filter_prefixes(
        prefixes,
        ipv4=args.ipv4,
        ipv6=args.ipv6,
    )

    for prefix in prefixes:
        print(prefix)


if __name__ == "__main__":
    main()
