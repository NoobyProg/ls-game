import discord
import json # Temporarily using JSON to store token, will change soon.

with open('config.json') as f:
    data = json.load(f)

client = discord.Client()

@client.event
async def on_ready():
    print('{} is ready'.format(client.user.name))

client.run(data["token"])