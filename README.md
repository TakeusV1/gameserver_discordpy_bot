# gameserver_discordpy_bot
### Dependencies
`pip3 install discord.py`<br>
`pip3 install mcstatus sourceserver`<br>

### Config
`token = 'xxxxxxxxxxxxxxx'`<br>
`server_ip = 'xx.xx.xx.xx'`<br>
`server_port = 'xxxxx'`<br>
`mcOs = True`<br>
### Prod
```bash
### Setup
apt update
curl -sL https://deb.nodesource.com/setup_18.x | sudo bash -
apt install nodejs -y
npm install pm2@latest -g
### Usage
pm2 start app.py --interpreter python3  # Pour démarrer le BOT
pm2 stop app.py # Pour stopper le BOT
pm2 monit # Pour voir les instances lancées (leurs logs...)
pm2 save # Pour lancer les instances à chaque démarrage du système
```
## Example
![1](https://user-images.githubusercontent.com/68923554/214927457-e3a14c35-9b73-4987-9c83-2ef74242cf37.png)<br>
![2](https://user-images.githubusercontent.com/68923554/214927480-1c54e7d3-b734-4e6d-90bb-9f515361576e.png)
