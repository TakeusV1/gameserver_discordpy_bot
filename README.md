# mcquery_discordpy_bot

### Dépendances
`pip install discord.py`<br>
`pip install mcstatus`

### Configuration
Il faut modifier les lignes suivantes:<br>
`token = 'xxxxxxxxxxxxxxx'`<br>
`server_ip = 'xx.xx.xx.xx'`<br>
`server_port = 'xxxxx'`

### Mise en PROD
On peut utiliser par exemple **PM2**:
```bash
## Installation
apt update
curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
apt install nodejs -y
npm install pm2@latest -g
## Utilisation
pm2 start app.js --interpreter python3  # Pour démarrer le BOT
pm2 stop app.js # Pour stopper le BOT
pm2 monit # Pour voir les instances lancées (leurs logs...)
pm2 save # Pour lancer les instances à chaque démarrage du système
```
