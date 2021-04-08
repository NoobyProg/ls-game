# Module Imports
import discord
import sqlite3
from discord.ext import commands
import string
import random

# Creates a connection to the SQLite Database where the records are stored
con = sqlite3.connect('Database/games.db')
cur = con.cursor()

game_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) # Used to generate a 6 digit random ID (String) with lowercase letters and numbers. For Example :- 6vt9y4

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Async function to check if the author is already entered in a record
    async def check_inGame(self, ctx):
        check = cur.execute('SELECT * FROM players WHERE playerId = "{}"'.format(ctx.author.id))
        if check.fetchone():
            return True
        else:
            return False

    # Used to create a New L's Game
    @commands.command()
    async def create(self, ctx):
        if await self.check_inGame(ctx) == True:
            await ctx.send('You have already joined another game')
        else:
            # Adds the Author's data into the database
            cur.execute('INSERT INTO players (playerId, gameId) VALUES ("{}", "{}")'.format(ctx.author.id, game_id))
            cur.execute('INSERT INTO games (masterId, gameId, guildId, "state") VALUES ("{}", "{}", "{}", "pre-game")'.format(ctx.author.id, game_id, ctx.guild.id))

            await ctx.send('An L\'s Game has been created with Game ID : **{}**'.format(game_id))

            con.commit()
    
    # Used to join an existing game
    @commands.command()
    async def join(self, ctx):
        if await self.check_inGame(ctx) == True:
            await ctx.send('You have already joined another game')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = '{}'".format(ctx.guild.id)).fetchone()[0]
            cur.execute('INSERT INTO players (playerId, gameId) VALUES ("{}", "{}")'.format(ctx.author.id, g_id))

            await ctx.send('Sucessfully joined L\'s Game with Game ID : **{}**'.format(g_id))
            con.commit()

def setup(bot):
    bot.add_cog(SetupCog(bot))