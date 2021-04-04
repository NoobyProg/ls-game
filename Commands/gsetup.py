import discord
import sqlite3
from discord.ext import commands

con = sqlite3.connect('Database/games.db')
cur = con.cursor()

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_inGame(self, ctx):
        check = cur.execute('SELECT * FROM players WHERE playerId = "{}"'.format(ctx.author.id))
        if check.fetchone():
            return True
        else:
            return False
    

    @commands.command()
    async def create(self, ctx):
        if await self.check_inGame(ctx) == True:
            await ctx.send("You have already joined another game")
        else:
            cur.execute("INSERT INTO players (playerId) VALUES ({})".format(ctx.author.id))
            cur.execute("INSERT INTO games (masterId) VALUES ({})".format(ctx.author.id))

            await ctx.send("An L's Game has been created")

            con.commit()

def setup(bot):
    bot.add_cog(SetupCog(bot))