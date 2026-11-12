#!/usr/bin/env bash
# Clones the five Idiotation blocks into blocks/ (gitignored, optional at runtime).
set -u
BLOCKS_DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)/blocks}"
mkdir -p "$BLOCKS_DIR"

clone() {
  local name="$1" url="$2" branch="$3" license="$4"
  if [ -d "$BLOCKS_DIR/$name" ]; then
    echo "[skip] $name already present"
    return
  fi
  echo "[clone] $name ($license)"
  if [ -n "$branch" ]; then
    git clone --depth 1 -b "$branch" "$url" "$BLOCKS_DIR/$name"
  else
    git clone --depth 1 "$url" "$BLOCKS_DIR/$name"
  fi
}

clone firecrawl     https://github.com/firecrawl/firecrawl       ""           "AGPL-3.0 (external tool only, never vendored)"
clone superpowers   https://github.com/obra/superpowers          ""           "MIT"
clone maxxing-itout https://github.com/Tulip9ZZZA/maxxing-itout  v2-gauntlet  "MIT"
clone roast-room    https://github.com/nateherkai/roast-room     ""           "MIT"
clone llm-council   https://github.com/karpathy/llm-council      ""           "NONE - clone for the visual app only; no code/text copied into Idiotation"

echo
echo "Done. Blocks live in $BLOCKS_DIR (gitignored)."
echo "All skills work WITHOUT the blocks - each SKILL.md embeds a native fallback."
