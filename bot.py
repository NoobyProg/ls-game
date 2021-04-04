import discord
from discord.ext import commands
import json # Temporarily using JSON to store token, will change soon.

with open('config.json') as f:
    data = json.load(f)

PREFIX = '%'

bot = commands.AutoShardedBot(command_prefix = PREFIX)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("L's Game"))
    print('{} is ready'.format(bot.user.name))

@bot.command()
@commands.is_owner()
async def load(ctx, *, module : str):
    try:
        bot.load_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module Loaded.'.format(module))
    
@bot.command()
@commands.is_owner()
async def unload(ctx, *, module : str):
    try:
        bot.unload_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module unloaded.'.format(module))

@bot.command(name='reload')
@commands.is_owner()
async def _reload(ctx, *, module : str):
    try:
        bot.reload_extension(module)
    except Exception as e:
        await ctx.send('`{}:` {}'.format(type(e).__name__, e))
    else:
        await ctx.send('`{}` Module reloaded.'.format(module))

@bot.command()
async def shutdown(ctx):
    await ctx.send('Shutting down')
    await bot.logout()

# Cogs Setup
initial_extensions = []

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
        print('Loaded {}'.format(extension))

bot.run(data["token"])