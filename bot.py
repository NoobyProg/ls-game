# Module Imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Loads .env file
load_dotenv()

PREFIX = '%'

bot = commands.AutoShardedBot(command_prefix = PREFIX)

# Changes bot presense and activity on login/ready
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("L's Game"))
    print('{} is ready'.format(bot.user.name))

# Used to load a Cog (Module)
@bot.command()
@commands.is_owner() # Makes the Command Bot Owner-only
async def load(ctx, *, module : str):
    try:
        bot.load_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module Loaded.'.format(module))
    
# Used to unload a Cog
@bot.command()
@commands.is_owner()
async def unload(ctx, *, module : str):
    try:
        bot.unload_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module unloaded.'.format(module))

# Reloads a Cog (Imitates a Cog Unload and Load)
@bot.command(name='reload')
@commands.is_owner()
async def _reload(ctx, *, module : str):
    try:
        bot.reload_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module reloaded.'.format(module))

# Used to completely shut down all shards of the bot
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shutting down')
    await bot.logout()

# Cogs Setup
initial_extensions = ['Commands.gsetup']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
        print('Loaded {}'.format(extension))

bot.run(os.getenv("DISCORD_TOKEN"))