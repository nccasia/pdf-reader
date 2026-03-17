#!/bin/bash
set -euo pipefail

# Default values
port=1300
host="0.0.0.0"
service_name="extract_cv.service"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--port) port="$2"; shift ;;
        -host|--host) host="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

current_directory=$(pwd)

# Set up virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Generate systemd service file
cat > "$service_name" <<EOF
[Unit]
Description=CV Extraction API Service

[Service]
User=root
EnvironmentFile=$current_directory/.env
WorkingDirectory=$current_directory
ExecStart=$current_directory/venv/bin/uvicorn app.main:app --host $host --port $port --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Install and start the service
sudo cp "$service_name" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start "$service_name"
sudo systemctl enable "$service_name"

echo "Service is running on http://$host:$port"
