#!/usr/bin/env bash
# NOTARIUS updater for macOS / Linux — fetches the latest version from GitHub
# into the folder this script lives in. Stop the app first (Ctrl+C).
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
URL="https://github.com/Rus1978Rus/Notarius/archive/refs/heads/main.zip"
TMP="$(mktemp -d)"

echo "Downloading the latest version..."
curl -L "$URL" -o "$TMP/notarius.zip"
echo "Extracting..."
( cd "$TMP" && unzip -q notarius.zip )
echo "Installing over $DIR ..."
# copy everything except this running script
( cd "$TMP/Notarius-main" && find . -type f ! -name update.sh -print0 \
    | while IFS= read -r -d '' f; do mkdir -p "$DIR/$(dirname "$f")"; cp "$f" "$DIR/$f"; done )
rm -rf "$TMP"
echo "Done. Start the app again with:  python3 -m notarius web"
