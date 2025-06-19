#!/bin/bash

#? THIS SHOULD WORK FOR LINUX

APP_NAME="flask-notifier"
APP_USER="$(whoami)"
APP_DIR="$(pwd)/src/main/notifier"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
VENV_PATH="/full/path/to/venv"

echo "Setting up Flask notifier service..."

# Install Gunicorn if not installed
if ! command -v gunicorn &> /dev/null; then
    echo "Installing Gunicorn..."
    pip3 install gunicorn
else
    echo "Gunicorn already installed."
fi

# Create systemd service file
echo "Creating systemd service file at $SERVICE_FILE ..."

sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Flask Notifier Service
After=network.target

[Service]
User=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=$VENV_PATH/bin/gunicorn -w 4 -b 127.0.0.1:5000 notifier:app
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon and enable/start service
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling and starting $APP_NAME service..."
sudo systemctl enable $APP_NAME
sudo systemctl start $APP_NAME

echo "Setup complete! Check status with:"
echo "  sudo systemctl status $APP_NAME"
