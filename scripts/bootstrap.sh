#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

clone_and_patch() {
  local url="$1"
  local destination="$2"
  local revision="$3"
  local patch="$4"

  if [[ ! -d "$destination/.git" ]]; then
    git clone --depth 1 --no-checkout "$url" "$destination"
    git -C "$destination" fetch --depth 1 origin "$revision"
    git -C "$destination" checkout --detach "$revision"
    git -C "$destination" submodule update --init --recursive --depth 1
  fi

  if [[ "$(git -C "$destination" rev-parse HEAD)" != "$revision" ]]; then
    printf 'Unexpected source revision in %s\n' "$destination" >&2
    exit 1
  fi
  if git -C "$destination" apply --reverse --check "$patch"; then
    printf 'Soul changes already present: %s\n' "$destination"
  else
    git -C "$destination" apply --check "$patch"
    git -C "$destination" apply "$patch"
    printf 'Applied Soul changes: %s\n' "$destination"
  fi
}

clone_and_patch \
  https://github.com/DrKLO/Telegram.git \
  "$project_dir/android" \
  f2908b14133bbffbf7ab04f641ecb5bfaf533242 \
  "$project_dir/patches/android.patch"

clone_and_patch \
  https://github.com/telegramdesktop/tdesktop.git \
  "$project_dir/desktop" \
  6fed91ffab9861771a75f29df65031b3c80b6941 \
  "$project_dir/patches/desktop.patch"
