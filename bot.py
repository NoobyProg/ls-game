import discord

TOKEN = ''

client = discord.Client()

@client.event
async def on_ready():
    print('{} is ready'.format(client.user.name))

client.run('')