"""Allow only stable MAJOR.MINOR.PATCH tags, optionally prefixed with v."""

import os
import re
from typing import Optional


STABLE_TAG = re.compile(r"v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def release_version(tag: str) -> Optional[str]:
    if STABLE_TAG.fullmatch(tag):
        return tag.removeprefix("v")
    return None


def main():
    tag = os.environ["GITHUB_REF_NAME"]
    version = release_version(tag) if os.environ["GITHUB_REF_TYPE"] == "tag" else None
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
        output.write(f"version={version or ''}\n")
    if version:
        print(f"Releasing {tag} as version {version}")
    else:
        print(f"Skipping {tag!r}: a stable semantic-version tag is required.")


if __name__ == "__main__":
    main()
