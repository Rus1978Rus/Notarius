#!/usr/bin/env bash
# NOTARIUS package-artifact generator (clearing debt AD-15).
# Real SHA-256 over git-tracked files. Hashes are never fabricated.
# Reproducible: re-running refreshes MANIFEST.tsv and SHA256SUMS.txt.
#
# Parent (E-Continuity) rules:
#   - hash only files that physically exist;
#   - SHA256SUMS does not hash itself (that would be self-reference);
#   - MANIFEST lists everything, including itself and SHA256SUMS.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

PKG="docs/_package"
MANIFEST="$PKG/MANIFEST.tsv"
SUMS="$PKG/SHA256SUMS.txt"

# List of tracked files, excluding the computed artifacts themselves.
mapfile -t FILES < <(git -c core.quotepath=false ls-files | grep -v -e "^$MANIFEST$" -e "^$SUMS$" | sort)

# SHA256SUMS: real computation, format `sha256  path`.
: > "$SUMS"
for f in "${FILES[@]}"; do
  sha256sum "$f" >> "$SUMS"
done

# MANIFEST.tsv: path <tab> bytes <tab> sha256(short) <tab> origin_hint.
printf 'path\tbytes\tsha256_short\torigin_hint\n' > "$MANIFEST"
for f in "${FILES[@]}"; do
  bytes=$(wc -c < "$f" | tr -d ' ')
  short=$(sha256sum "$f" | cut -c1-12)
  case "$f" in
    docs/foundation_layer/*|docs/e_continuity/*) hint="COPY_FROM_AUTHOR_PACKAGE" ;;
    docs/vendor_answers/*)                       hint="EXTERNAL_VENDOR" ;;
    docs/NOTARIUS_FULL_SESSION.md)               hint="AUTHOR_SOURCE_PLUS_LLM_EDITS" ;;
    notarius/*|tests/*|experiments/*|scripts/*)  hint="LLM_GENERATED_CODE" ;;
    *)                                           hint="LLM_GENERATED_DOC" ;;
  esac
  printf '%s\t%s\t%s\t%s\n' "$f" "$bytes" "$short" "$hint" >> "$MANIFEST"
done

echo "MANIFEST:   $MANIFEST ($(( ${#FILES[@]} )) files)"
echo "SHA256SUMS: $SUMS"
echo "Verify:     cd \$(git rev-parse --show-toplevel) && sha256sum -c $SUMS"
