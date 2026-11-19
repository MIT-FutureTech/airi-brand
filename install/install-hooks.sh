#!/usr/bin/env bash
# Install git hooks that keep ~/.claude/skills/airi-brand in step with skill/.
# Safe to re-run.
#
#   post-commit: after a commit on main that touches skill/
#   post-merge:  after a pull or merge into main that touches skill/
#
# Both call install/sync-installed-skill.sh, which is tracked in the repo, so
# changes to the sync logic don't need the hooks reinstalled.

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
HOOK_DIR=$(git -C "$REPO_ROOT" rev-parse --git-path hooks)
case "$HOOK_DIR" in /*) ;; *) HOOK_DIR="$REPO_ROOT/$HOOK_DIR" ;; esac
mkdir -p "$HOOK_DIR"

cat > "$HOOK_DIR/post-commit" <<'HOOK'
#!/usr/bin/env bash
# Installed by install/install-hooks.sh. Edit there, not here.
REPO_ROOT=$(git rev-parse --show-toplevel)
if git diff-tree --no-commit-id --name-only -r --root HEAD | grep -q '^skill/'; then
  "$REPO_ROOT/install/sync-installed-skill.sh" || echo "airi-brand: skill sync failed (commit kept)" >&2
fi
HOOK

cat > "$HOOK_DIR/post-merge" <<'HOOK'
#!/usr/bin/env bash
# Installed by install/install-hooks.sh. Edit there, not here.
REPO_ROOT=$(git rev-parse --show-toplevel)
if git diff --name-only ORIG_HEAD HEAD 2>/dev/null | grep -q '^skill/'; then
  "$REPO_ROOT/install/sync-installed-skill.sh" || echo "airi-brand: skill sync failed (merge kept)" >&2
fi
HOOK

chmod +x "$HOOK_DIR/post-commit" "$HOOK_DIR/post-merge" "$SCRIPT_DIR/sync-installed-skill.sh"
echo "installed: $HOOK_DIR/post-commit, $HOOK_DIR/post-merge"
