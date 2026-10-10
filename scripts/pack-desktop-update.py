#!/usr/bin/env python3
"""Pack a signed Soul Desktop update with Telegram Desktop's Packer."""

import argparse
import os
import subprocess
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
KEYS = PROJECT / "desktop/Telegram/Resources/update"
DEFAULT_KEY = Path.home() / ".local/share/Soul/signing/release-private.pem"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packer", required=True, type=Path,
                        help="compiled Packer or Packer.exe")
    parser.add_argument("--version", required=True, type=int,
                        help="numeric AppVersion from Desktop source")
    parser.add_argument("--target", choices=("win", "win64", "winarm", "mac", "linux"),
                        required=True)
    parser.add_argument("--arch", choices=("x86_64", "arm64"),
                        help="required for macOS packages")
    parser.add_argument("--file", action="append", required=True, type=Path,
                        help="file or directory included in the update; repeat as needed")
    parser.add_argument("--key", type=Path,
                        default=Path(os.environ.get("SOUL_RELEASE_KEY", DEFAULT_KEY)))
    args = parser.parse_args()

    if args.version <= 0:
        parser.error("--version must be positive")
    if args.target == "mac" and args.arch is None:
        parser.error("--arch is required for macOS")
    if args.target != "mac" and args.arch is not None:
        parser.error("--arch is only for macOS")
    if not args.packer.is_file():
        parser.error("--packer must point to a compiled Packer")
    if not args.key.is_file():
        parser.error("Soul release signing key not found")
    if any(not path.exists() for path in args.file):
        parser.error("every --file path must exist")

    command = [str(args.packer.resolve())]
    for path in args.file:
        command.extend(("-path", str(path.resolve())))
    command.extend((
        "-version", str(args.version),
        "-channel", "stable",
        "-keys-loc", str(KEYS),
        "-local-key", str(args.key.resolve()),
        "-local-key-id", "soul-2026a",
    ))
    if args.target != "linux":
        command.extend(("-target", args.target))
    if args.arch:
        command.extend(("-arch", args.arch))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
