# asn2cidr

Print an ASN's announced IP prefixes using RIPEstat.

## Install

Requires Python 3.9 or newer and an internet connection to query RIPEstat.

### PyPI

```sh
pipx install asn2cidr
```

Alternatively, install with pip in a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install asn2cidr
```

### Debian / Ubuntu

Download the `.deb` from [GitHub Releases](https://github.com/mateuszmikrut/asn2cidr/releases),
then install it with apt so that Python and Requests are installed as dependencies:

```sh
sudo apt install ./asn2cidr_1.2.3-1_all.deb
```

Replace the example filename with the version you downloaded.

### Fedora / RPM-based distributions

Download the `.rpm` from [GitHub Releases](https://github.com/mateuszmikrut/asn2cidr/releases),
then install it with your distribution's package manager:

```sh
sudo dnf install ./asn2cidr-1.2.3-1.noarch.rpm
```

Both Linux packages are architecture-independent and use the distribution's
Python 3.9+ and `python3-requests` packages. The workflow checks installation on
Debian 12 and Fedora 43.

### From source

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
```

## Usage

Pass the ASN as the first argument, without the `AS` prefix. Both IPv4 and
IPv6 prefixes are printed by default, one per line.

```sh
asn2cidr 13335
asn2cidr 13335 --ipv4
asn2cidr 13335 --ipv6
```

The short options `-4` and `-6` are also supported. `asn2cidr --asn 13335`
accepts the ASN as an option. Supply the ASN once and choose at most one
address-family option.
