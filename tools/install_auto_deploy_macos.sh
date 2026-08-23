#!/bin/bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
LABEL="it.sistema90g.site-autodeploy"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG_DIR="$HOME/Library/Logs/Sistema90G"
mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$ROOT/tools/auto_deploy_watch.sh</string>
  </array>
  <key>StartInterval</key><integer>120</integer>
  <key>RunAtLoad</key><true/>
  <key>EnvironmentVariables</key>
  <dict><key>S90G_SITE_ROOT</key><string>$ROOT</string></dict>
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
launchctl print "gui/$(id -u)/$LABEL" | head -40
