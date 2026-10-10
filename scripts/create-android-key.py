#!/usr/bin/env python3
"""Create a local Android signing key for Soul without printing its password."""

import os
import secrets
import subprocess
from pathlib import Path


def main() -> None:
    os.umask(0o077)
    directory = Path.home() / ".local/share/Soul/signing"
    key = directory / "android-release.p12"
    properties = directory / "android.properties"
    directory.mkdir(parents=True, exist_ok=True)
    os.chmod(directory, 0o700)
    if key.exists() or properties.exists():
        raise SystemExit("Soul Android signing key already exists; left unchanged")

    password = secrets.token_urlsafe(36)
    command = [
        "keytool", "-genkeypair", "-noprompt", "-storetype", "PKCS12",
        "-keystore", str(key), "-storepass", password, "-keypass", password,
        "-alias", "soul", "-keyalg", "RSA", "-keysize", "4096",
        "-validity", "10000", "-dname", "CN=Soul,O=Soul,C=US",
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        properties.write_text(
            f"storeFile={key}\nstorePassword={password}\n"
            f"keyAlias=soul\nkeyPassword={password}\n", encoding="utf-8"
        )
        os.chmod(key, 0o600)
        os.chmod(properties, 0o600)
    except Exception:
        key.unlink(missing_ok=True)
        properties.unlink(missing_ok=True)
        raise
    print(f"Created Soul Android signing key in {directory}")


if __name__ == "__main__":
    main()
