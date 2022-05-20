import discord
from asyncio import sleep
from discord.ext import tasks, commands
from mcstatus import JavaServer

## Config
token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Token BOT
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

@tasks.loop(seconds=5)
async def loop():
    try:
        server = JavaServer.lookup(str(server_ip+':'+server_port))
        status = server.status()
        if status.players.online == 0:
            await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)),status=discord.Status.idle)
        else:
            await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)),status=discord.Status.online)

    except:
        await bot.change_presence(activity=discord.Game(name="Serveur Hors-Ligne"),status=discord.Status.dnd)

@bot.command()
async def info(ctx):
    try:
        server = JavaServer.lookup(str(server_ip+':'+server_port))
        status = server.status()
        await ctx.channel.send("__**Joueurs**__: {}/{}\n__**Latence**__: {} *ms*".format(status.players.online,status.players.max,server.ping()))
    except:
        await ctx.channel.send("Serveur Hors-Ligne")

@bot.command()
async def cmd(ctx):
    await ctx.channel.send(f"__**Liste des Commandes**__:\n {bot_prefix}info *(Affiche les informations du Serveur)*")

@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'Bot UP !\nLatence: {round(bot.latency, 1)}')

bot.run(token)

## Takeus 2022
