# cron

Auto Restart Everyday at `00:00`

```
sudo crontab -e
```

add :

```
0 0 * * * /sbin/shutdown -r now
```

```
sudo systemctl enable cron
sudo systemctl start cron
```