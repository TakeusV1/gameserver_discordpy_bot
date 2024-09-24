# gameserver_discordpy_bot
### Dependencies
- mcstatus
- sourceserver
### Config
`token = 'xxxxxxxxxxxxxxx'`<br>
`server_ip = 'xx.xx.xx.xx'`<br>
`server_port = 'xxxxx'`<br>
`mcOs = True`<br>
### Installation
##### Python
```bash
python -m venv discord_bot
source discord_bot/bin/activate
pip install discord.py
pip install mcstatus sourceserver
deactivate
```
##### Production
You can setup a systemd service or do the following with “pm2” :<br>
(which lets you manage your instances very easily with access to logs, console...)
```bash
### Setup
apt update
curl -sL https://deb.nodesource.com/setup_18.x | sudo bash -
apt install nodejs -y
npm install pm2@latest -g
### Usage
pm2 start app.py --interpreter python3  # To start the BOT
pm2 stop app.py # To stop the BOT
pm2 monit # To see the launched instances
pm2 save && pm2 startup # To launch the instances at each system startup
```
## Example
![1](https://user-images.githubusercontent.com/68923554/214927457-e3a14c35-9b73-4987-9c83-2ef74242cf37.png)<br>
![2](https://user-images.githubusercontent.com/68923554/214927480-1c54e7d3-b734-4e6d-90bb-9f515361576e.png)
