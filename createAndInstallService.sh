#!/bin/bash

echo "[Unit]
Description=Raspberry Pi Zero Display
After=network.target

[Service]
Type=exec
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 $(pwd)/main.py --serve-in-foreground
Restart=on-failure

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/pi-display.service && \
systemctl start pi-display.service && \
systemctl enable pi-display.service