import discord
from asyncio import sleep
from discord.ext import tasks, commands
from mcstatus import JavaServer

## Config
token = 'xxxxxxxxxxxxxxx' # Token BOT
server_ip = 'xx.xx.xx.xx' # Addresse IP 
server_port = 'xxxxx' # Port
bot_prefix = '!!' # Préfixe

bot = discord.Client()
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
    if not loop.is_running():
        loop.start()
    print('Ready')

@tasks.loop(seconds=2)
async def loop():
    server = JavaServer.lookup(str(server_ip+':'+server_port))
    status = server.status()
    await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)))

@bot.command()
async def info(ctx):
    server = JavaServer.lookup(str(server_ip+':'+server_port))
    status = server.status()
    await ctx.channel.send("__**Joueurs**__: {}/{}\n__**Latence**__: {} *ms*".format(status.players.online,status.players.max,server.ping()))

@bot.command()
async def cmd(ctx):
    await ctx.channel.send(f"__**Liste des Commandes**__:\n {bot_prefix}info *(Affiche les informations du Serveur)*")

bot.run(token)

## Takeus 2022
