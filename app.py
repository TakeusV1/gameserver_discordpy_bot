import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, BotMissingPermissions
from discord.ext import tasks, commands
from mcstatus import JavaServer

## Config
token = 'xxxxxxxxxxxxxxx' # Token BOT
server_ip = 'xx.xx.xx.xx' # Addresse IP
server_port = 'xxxxx' # Port
bot_prefix = '!!' # Préfixe

## Pterodactyl Config
ptero_enable = False
if ptero_enable:
    ptero_link = 'https://ptero.example.fr' # FQDN De votre Pterodactyl
    ptero_clientapi = '' # Clé API de votre compte Pterodactyl
    ptero_serverid = '' # Identifiant (Abrégé) du serveur
    discord_admins_id = [] # Identifiant (Discord) des utilisateurs pouvant interagir avec les commandes...

#bot = discord.Client()
bot = commands.Bot(command_prefix=bot_prefix,intents = discord.Intents.all())

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
        server = JavaServer.lookup(str(server_ip+':'+server_port))
        status = server.status()
        if status.players.online == 0:
            await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)),status=discord.Status.idle)
        else:
            await bot.change_presence(activity=discord.Game(name="{}/{} Joueurs".format(status.players.online,status.players.max)),status=discord.Status.online)

    except:
        await bot.change_presence(activity=discord.Game(name="Serveur Hors-Ligne"),status=discord.Status.dnd)

@bot.tree.command(name="serverinfo", description="Affiche les informations du serveur.")
async def serverinfo(interaction: discord.Interaction):
    try:
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
    except:
        await interaction.response.send_message("Serveur Hors-Ligne")

@bot.tree.command(name="ping", description="latence du bot")
async def serverinfo(interaction: discord.Interaction):
    await interaction.response.send_message(f'Bot UP !\nLatence: {round(bot.latency, 1)}')

if ptero_enable:
    from pydactyl import PterodactylClient
    api = PterodactylClient(ptero_link, ptero_clientapi)
    #print(api.client.servers.get_server_utilization(ptero_serverid))

    @bot.command()
    async def sinfo(ctx):
        if ctx.author.id in discord_admins_id:
            infoserver = api.client.servers.get_server_utilization(ptero_serverid)
            if infoserver['current_state'] == 'offline':
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name='STATUS', value=infoserver['current_state'], inline=True)
                embed.add_field(name='DISK', value=str(round(float(infoserver['resources']['disk_bytes'])/1024/1024))+' MO', inline=True)
            else:
                if infoserver['current_state'] == 'starting':
                    embed=discord.Embed(color=0xffff00)
                else:
                    embed=discord.Embed(color=0x00ff00)
                embed.add_field(name='STATUS', value=infoserver['current_state'], inline=True)
                embed.add_field(name='CPU', value=str(round(infoserver['resources']['cpu_absolute']))+' %', inline=True)
                embed.add_field(name='RAM', value=str(round(float(infoserver['resources']['memory_bytes'])/1024/1024))+' MO', inline=True)
                embed.add_field(name='DISK', value=str(round(float(infoserver['resources']['disk_bytes'])/1024/1024))+' MO', inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.channel.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")
    
    @bot.command()
    async def power(ctx, arg):
        if ctx.author.id in discord_admins_id:
            if arg == 'start':
                api.client.servers.send_power_action(ptero_serverid,'start')
                await ctx.channel.send("Commande envoyé !")
            elif arg == 'stop':
                api.client.servers.send_power_action(ptero_serverid,'stop')
                await ctx.channel.send("Commande envoyé !")
            elif arg == 'kill':
                api.client.servers.send_power_action(ptero_serverid,'kill')
                await ctx.channel.send("Commande envoyé !")
            else:
                await ctx.channel.send("Argument invalide. Les options sont: **start, stop, kill**")
        else:
            await ctx.channel.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")

    @bot.command()
    async def console(ctx, arg):
        if ctx.author.id in discord_admins_id:
            api.client.servers.send_console_command(ptero_serverid,arg)
            await ctx.channel.send("Commande envoyé !")
        else:
            await ctx.channel.send("Vous n'avez pas l'autorisation d'utiliser cette commande.")

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Cette commande nécéssite un Argument.')

bot.run(token)

## Takeus 2023