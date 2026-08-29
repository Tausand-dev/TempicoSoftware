#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
DEST="/Applications/TempicoSoftware.app"
echo "Installing TempicoSoftware..."
rm -rf "$DEST"
ditto "TempicoSoftware.app" "$DEST"
for i in $(seq 1 20); do
  if [ -x "$DEST/Contents/MacOS/TempicoSoftware" ]; then
    break
  fi
  sleep 0.5
done

xattr -cr "$DEST"

echo "Done. Opening TempicoSoftware..."
open "$DEST"

rm -rf "$SCRIPT_DIR/TempicoSoftware.app"
sleep 1
rm -f "$0"
