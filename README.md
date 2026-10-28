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

The original script remains available as `python ans2cidr.py 13335` from a
checkout with its dependencies installed.

## Releases

The [release workflow](.github/workflows/release.yml) runs on pushed tags. Only
stable semantic versions of the form `MAJOR.MINOR.PATCH`, optionally prefixed
with a lowercase `v`, can build packages, publish to PyPI, or create a GitHub
release. Version components must not have leading zeroes (except `0` itself).

| Tag | Result |
| --- | --- |
| `1.2.3`, `v1.2.3`, `v0.1.0` | Build, publish, and release |
| `1.2.3-rc.1`, `v1.2.3-beta`, `1.2.3-label` | Skip |
| `1.2.3+build.4`, `v1.2.3-rc.1+build.4` | Skip |
| `1.2`, `v01.2.3`, `release-1.2.3` | Skip |

GitHub's tag filters use globs, so ineligible tags may show a successful
validation job; all package-building, publishing, and release jobs are skipped.
Branch pushes and manual runs do not trigger this workflow.

Each eligible tag produces a Python wheel and source archive, a `.deb`, an
`.rpm`, and `SHA256SUMS`. The GitHub release page includes generated release
notes and all these assets. Only the wheel and source archive go to PyPI.
Both publishing jobs wait for package validation, then run independently.
The normalized tag supplies the Python version (`v1.2.3` becomes `1.2.3`);
Linux packages add package revision `1` (`1.2.3-1`).

### One-time PyPI setup

Create the `pypi` environment under this repository's GitHub **Settings → Environments**.
On PyPI, add a [Trusted Publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
to the `asn2cidr` project. If the project does not yet exist, create a pending
publisher with that project name. Use these exact values:

| Setting | Value |
| --- | --- |
| Owner | `mateuszmikrut` |
| Repository | `asn2cidr` |
| Workflow filename | `release.yml` |
| Environment | `pypi` |

The workflow uses GitHub's OIDC identity, so no PyPI API token secret is needed.
GitHub releases use the workflow's built-in `GITHUB_TOKEN`.

### Publish a version

Commit and push the release changes first, then tag the intended commit:

```sh
git tag -a v1.2.3 -m "Release 1.2.3"
git push origin v1.2.3
```

An unprefixed tag such as `1.2.3` works too. Choose one spelling per version:
both normalize to the same PyPI version, and PyPI does not allow overwriting an
uploaded distribution. Use a new version for subsequent releases.

### Local checks and builds

```sh
python -m unittest discover -s tests -v
python -m pip install build twine
SETUPTOOLS_SCM_PRETEND_VERSION=1.2.3 python -m build
python -m twine check --strict dist/*
```

For native packages, install [nFPM](https://nfpm.goreleaser.com/install/)
(the workflow pins version 2.48.0), then run from the repository root:

```sh
mkdir -p dist
VERSION=1.2.3 nfpm package --config packaging/nfpm.yaml --packager deb --target dist/
VERSION=1.2.3 nfpm package --config packaging/nfpm.yaml --packager rpm --target dist/
```
