#!/bin/bash
# setup_service.bash
# This script deploys the sertAI systemd service.

# Get the current repository directory
REPO_DIR=$(pwd)
echo "Detected repository directory: $REPO_DIR"

SERVICE_FILE="deploy/sertAI@.service"
DESTINATION="/etc/systemd/system/sertAI@.service"

if [ ! -f "$SERVICE_FILE" ]; then
  echo "Service file not found: $SERVICE_FILE"
  exit 1
fi

# Replace the placeholder %REPO_DIR% with the actual repository directory.
sed -i "s|%REPO_DIR%|$REPO_DIR|g" "$SERVICE_FILE"

echo "Copying service file to $DESTINATION..."
sudo cp "$SERVICE_FILE" "$DESTINATION"

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling the service to start on boot..."
sudo systemctl enable sertAI@$(whoami).service

echo "Starting the service..."
sudo systemctl start sertAI@$(whoami).service

echo "Service deployed and started. Check its status with:"
echo "  sudo systemctl status sertAI@$(whoami).service"