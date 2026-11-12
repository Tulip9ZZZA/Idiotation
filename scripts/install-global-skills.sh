#!/usr/bin/env bash
# Installs frequently-used skills at GLOBAL level for OpenCode:
# brand-skills, logo-design, beautify-github-readme, Matt Pocock's engineering skills.
# Usage: install-global-skills.sh <dir-with-extracted-packs>
set -u
SRC="${1:?Usage: install-global-skills.sh <dir-with-extracted-packs>}"
TARGET="$HOME/.config/opencode/skills"
mkdir -p "$TARGET"

find_pack() { # $1 = stem
  find "$SRC" -maxdepth 4 -type d -name "*$1*" | while read -r d; do
    if [ -d "$d/skills" ]; then echo "$d"; return 0; fi
  done | head -n 1
}

install_pack() { # $1 = stem, $2 = subfolder (relative)
  local pack sub root id
  pack="$(find_pack "$1")"
  if [ -z "$pack" ]; then echo "[warn] pack '$1' not found"; return; fi
  if [ -n "${2:-}" ]; then root="$pack/$2"; else root="$pack/skills"; fi
  if [ ! -d "$root" ]; then echo "[warn] missing $root"; return; fi
  for d in "$root"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    id="$(basename "$d")"
    rm -rf "$TARGET/$id"
    cp -r "$d" "$TARGET/$id"
    echo "  [global] $id"
  done
}

echo "== Installing global skills to $TARGET =="
echo "-- brand-skills (Cofoundy SAC, MIT; naming adapted from glacierphonk/naming) --"
install_pack "brand-skills" "skills"
echo "-- logo-design (kaankiziltug, MIT) --"
install_pack "logo-design-skill" "skills"
echo "-- beautify-github-readme (oil-oil, MIT) --"
install_pack "beautify-github-readme" "skills"
echo "-- matt-pocock skills (Matt Pocock, MIT) - engineering + productivity --"
install_pack "skills-main" "skills/engineering"
install_pack "skills-main" "skills/productivity"

mkdir -p "$TARGET/_credits"
cat > "$TARGET/_credits/ATTRIBUTION.md" <<'EOF'
# Global skill attributions

Installed at global level by Idiotation (scripts/install-global-skills.sh).
All packs copied as-is, unmodified, under their MIT licenses.

- brand-skills/* - MIT (c) 2026 Cofoundy SAC
  skills/naming/ adapted from glacierphonk/naming - MIT (c) 2026 GlacierPhonk
- logo-design - MIT (c) 2026 kaankiziltug
- beautify-github-readme - MIT (c) 2026 oil-oil
- engineering/* and productivity/* - MIT (c) 2026 Matt Pocock (mattpocock/skills)
EOF

echo
echo "Done. New OpenCode sessions (any folder) now advertise these skills."
