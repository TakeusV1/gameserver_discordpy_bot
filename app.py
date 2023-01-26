import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, BotMissingPermissions
from discord.ext import tasks, commands

## Config
token = 'xxxxxxxxxxxxxxx' # Token BOT
server_ip = 'xx.xx.xx.xx' # Addresse IP 
server_port = 'xxxxx' # Port
mcOs = True #IF True = Minecraft Serve OR IF False = Source Server (like gmod,csgo...)

bot = commands.Bot(command_prefix='!!',intents = discord.Intents.default())

if mcOs:
    from mcstatus import JavaServer
else:
    from sourceserver.sourceserver import SourceServer

@bot.event
async def on_ready():
    if not loop.is_running():
        loop.start()
    print('Ready')
    ## commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@tasks.loop(seconds=5)
async def loop():
    try:
        # minecraft server
        if mcOs:
            server = JavaServer.lookup(str(server_ip+':'+server_port))
            status = server.status()
            if status.players.online == 0:
                await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)),status=discord.Status.idle)
            else:
                await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)),status=discord.Status.online)
        else:
            # source server
            srv = SourceServer(str(server_ip+':'+server_port))
            if int(srv.info['players']) == 0:
                await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(srv.info['players'],srv.info['max_players'])),status=discord.Status.idle)
            else:
                await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(srv.info['players'],srv.info['max_players'])),status=discord.Status.online)

    except:
        await bot.change_presence(activity=discord.Game(name="Serveur Hors-Ligne"),status=discord.Status.dnd)

@bot.tree.command(name="serverinfo", description="Affiche les informations du serveur.")
async def serverinfo(interaction: discord.Interaction):
    try:
        # minecraft server
        if mcOs:
            server = JavaServer.lookup(str(server_ip+':'+server_port))
            status = server.status()
            #await ctx.channel.send("__**Joueurs**__: {}/{}\n__**Latence**__: {} *ms*".format(status.players.online,status.players.max,server.ping()))
            embed=discord.Embed(color=0xff8000)
            embed.add_field(name='Joueurs', value=status.players.online, inline=True)
            embed.add_field(name='Slots', value=status.players.max, inline=True)
            embed.add_field(name='Latence', value=str(status.latency)+' ms', inline=True)
            embed.add_field(name='Addresse', value=server_ip, inline=True)
            embed.add_field(name='Port', value=server_port, inline=True)
            embed.add_field(name='Version', value=status.version.name, inline=True)
            await interaction.response.send_message(embed=embed)
        # source server
        else:
            srv = SourceServer(str(server_ip+':'+server_port))
            embed=discord.Embed(title=srv.info['name'], color=0x0080ff)
            embed.add_field(name='Joueurs', value=srv.info['players'], inline=True)
            embed.add_field(name='Slots', value=srv.info['max_players'], inline=True)
            embed.add_field(name='Latence', value=srv.ping(2), inline=True)
            embed.add_field(name='Gamemode', value=srv.info['game'], inline=True)
            embed.add_field(name='Map', value=srv.info['map'], inline=True)
            embed.add_field(name='Version', value=srv.info['version'], inline=True)
            await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message("Serveur Hors-Ligne")

@bot.tree.command(name="ping", description="latence du bot")
async def serverinfo(interaction: discord.Interaction):
    await interaction.response.send_message(f'Bot UP !\nLatence: {round(bot.latency, 1)}')

bot.run(token)
## Takeus 2023