# systemd

Auto Restart Program

```
sudo nano /etc/systemd/system/price_wathcer.service
```

price_wathcer.service :

```
[Unit]
Description=Price Watcher Auto Start
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/home/ubuntu/price_watcher/.venv/bin/python /home/ubuntu/price_watcher/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl enable price_wathcer
sudo systemctl start price_wathcer
sudo systemctl status price_wathcer
```

check logging with :

```
journalctl -u price_wathcer -f
```