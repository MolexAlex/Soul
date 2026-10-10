#!/usr/bin/env python3
"""Create the Android update manifest to attach to a GitHub release."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, help="GitHub owner/repository")
    parser.add_argument("--tag", required=True, help="release tag")
    parser.add_argument("--version", required=True)
    parser.add_argument("--version-code", required=True, type=int)
    parser.add_argument("--apk", required=True, type=Path)
    parser.add_argument("--changelog", default="")
    parser.add_argument("--output", default="android-update.json", type=Path)
    args = parser.parse_args()

    if len(args.repository.split("/")) != 2 or not all(args.repository.split("/")):
        parser.error("--repository must be owner/repository")
    if args.version_code <= 0:
        parser.error("--version-code must be positive")
    if not args.apk.is_file() or args.apk.suffix.lower() != ".apk":
        parser.error("--apk must point to an APK file")

    with args.apk.open("rb") as apk_stream:
        digest = hashlib.file_digest(apk_stream, "sha256").hexdigest()
    url = (
        f"https://github.com/{args.repository}/releases/download/"
        f"{quote(args.tag, safe='')}/{quote(args.apk.name, safe='')}"
    )
    manifest = {
        "version": args.version,
        "version_code": args.version_code,
        "file_url": url,
        "sha256": digest,
        "changelog": args.changelog,
    }
    args.output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
