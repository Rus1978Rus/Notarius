#!/usr/bin/env bash
# NOTARIUS launcher for macOS / Linux — double-click or run in a terminal.
# Opens the local web app at http://127.0.0.1:8788. Ctrl+C to stop.
cd "$(dirname "$0")"
echo "Starting NOTARIUS... a browser window will open at http://127.0.0.1:8788"
echo "To stop: press Ctrl+C."
if command -v python3 >/dev/null 2>&1; then
  python3 -m notarius web
else
  echo "Python 3 was not found. Install it from https://www.python.org/downloads/ and try again."
  read -r -p "Press Enter to close..."
fi
