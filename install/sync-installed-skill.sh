#!/usr/bin/env bash
# Copy the committed skill/ folder to ~/.claude/skills/airi-brand as a plain
# folder, mirroring it exactly (files removed from skill/ are removed there too).
#
# Run by the post-commit and post-merge hooks that install-hooks.sh sets up,
# or by hand. Hooks only sync on main, so review branches don't install
# unmerged changes; run by hand with --force to sync from another branch.
#
# The destination must stay a real folder, not a symlink: it reaches other
# machines through a Syncthing share that doesn't carry symlinked content.

set -euo pipefail

REPO_ROOT=$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)
DEST="${AIRI_BRAND_SKILL_DEST:-$HOME/.claude/skills/airi-brand}"

if [ "${1:-}" != "--force" ]; then
  branch=$(git -C "$REPO_ROOT" symbolic-ref --quiet --short HEAD || true)
  if [ "$branch" != "main" ]; then
    exit 0
  fi
fi

if [ -L "$DEST" ]; then
  echo "airi-brand: $DEST is a symlink; not syncing (it must be a plain folder)" >&2
  exit 1
fi

# Export skill/ as committed in HEAD, so uncommitted edits never get installed.
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
git -C "$REPO_ROOT" archive HEAD skill | tar -x -C "$tmp"

mkdir -p "$DEST"
rsync -a --delete "$tmp/skill/" "$DEST/"
echo "airi-brand: installed skill synced to $DEST"
