#!/bin/bash
set -euo pipefail

LABEL="it.sistema90g.site-autodeploy"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$HOME/Library/Logs/Sistema90G"
AUTO_ROOT="$HOME/Library/Application Support/Sistema90G/Automation/site"
REMOTE="https://github.com/Gianca-64/sistema90g-site.git"
BRANCH="main"

mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR" "$(dirname "$AUTO_ROOT")"

if [ ! -d "$AUTO_ROOT/.git" ]; then
  git clone --branch "$BRANCH" --single-branch "$REMOTE" "$AUTO_ROOT"
else
  ACTUAL_REMOTE="$(git -C "$AUTO_ROOT" remote get-url origin)"
  if [[ "$ACTUAL_REMOTE" != *"Gianca-64/sistema90g-site.git"* ]]; then
    echo "ERRORE: il clone tecnico esistente non punta a Gianca-64/sistema90g-site" >&2
    exit 1
  fi
  if [ -n "$(git -C "$AUTO_ROOT" status --porcelain)" ]; then
    echo "ERRORE: working tree del clone tecnico non pulito" >&2
    exit 1
  fi
  git -C "$AUTO_ROOT" fetch origin
  git -C "$AUTO_ROOT" checkout "$BRANCH"
  git -C "$AUTO_ROOT" merge --ff-only "origin/$BRANCH"
fi

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$AUTO_ROOT/tools/auto_deploy_watch.sh</string>
  </array>
  <key>StartInterval</key><integer>120</integer>
  <key>RunAtLoad</key><true/>
  <key>EnvironmentVariables</key>
  <dict><key>S90G_SITE_ROOT</key><string>$AUTO_ROOT</string></dict>
  <key>StandardOutPath</key><string>$LOG_DIR/site-autodeploy-launchd.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/site-autodeploy-launchd.err.log</string>
</dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
launchctl enable "gui/$(id -u)/$LABEL"
launchctl kickstart -k "gui/$(id -u)/$LABEL"

echo "INSTALLATO: $LABEL"
echo "CLONE TECNICO: $AUTO_ROOT"
launchctl print "gui/$(id -u)/$LABEL" | head -40
