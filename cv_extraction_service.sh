#!/bin/bash
# Default values for port and host
port=1300
host="0.0.0.0"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--port) port="$2"; shift ;;
        -host|--host) host="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done
python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

current_directory=$(pwd)
echo "[Unit]" > extract_cv.service
echo "Description= CV information extraction Service" >> extract_cv.service
echo "[Service]" >> extract_cv.service
echo "User=root" >> extract_cv.service
echo "EnvironmentFile=$current_directory/.env" >> extract_cv.service
echo "WorkingDirectory=$current_directory" >> extract_cv.service
echo "ExecStart=$current_directory/venv/bin/uvicorn app.main:app --host $host --port $port --workers 2" >> extract_cv.service
echo "Restart=always" >> extract_cv.service
echo "RestartSec=3" >> extract_cv.service
echo "[Install]" >> extract_cv.service
echo "WantedBy=multi-user.target" >> extract_cv.service

sudo cp extract_cv.service /etc/systemd/system/

# Reload the service files to include the new service
sudo systemctl daemon-reload

# Start your service
sudo systemctl start extract_cv.service

# To enable your service on every reboot
sudo systemctl enable extract_cv.service

echo "The service is running"
