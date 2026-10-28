# asn2prefix

Print an ASN's announced IP prefixes using RIPEstat.

## Install

Requires Python 3.9 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Pass the ASN as the first argument, without the `AS` prefix. Both IPv4 and
IPv6 prefixes are printed by default, one per line.

```sh
python ans2prefix.py 13335
python ans2prefix.py 13335 --ipv4
python ans2prefix.py 13335 --ipv6
```

The short options `-4` and `-6` are also supported. The existing
`python ans2prefix.py --asn 13335` syntax still works. Supply the ASN once and
choose at most one address-family option.

An internet connection is required to query RIPEstat.
