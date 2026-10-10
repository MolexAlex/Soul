#!/usr/bin/env python3
"""Create Telegram Desktop compatible update feeds for Soul releases."""

import argparse
import json
from pathlib import Path


PLATFORMS = {"win", "win64", "winarm", "mac", "armac", "linux"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", type=int, required=True,
                        help="numeric AppVersion from desktop/core/version.h")
    parser.add_argument("--asset", action="append", required=True,
                        help="platform=update-package-name; repeat for each platform")
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    if args.version <= 0:
        parser.error("--version must be positive")
    feed = {}
    for item in args.asset:
        platform, separator, filename = item.partition("=")
        if not separator or platform not in PLATFORMS or platform in feed:
            parser.error(f"invalid or duplicate platform in --asset: {item}")
        if filename != Path(filename).name or not filename.startswith("td-update-"):
            parser.error(f"invalid update package name: {filename}")
        feed[platform] = {"stable": {"released": args.version, "link": "/" + filename}}

    args.output_dir.mkdir(parents=True, exist_ok=True)
    body = json.dumps(feed, separators=(",", ":")) + "\n"
    for version in (2, 6):
        (args.output_dir / f"current{version}").write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
