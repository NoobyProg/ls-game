# Module Imports
import discord
import sqlite3
from discord.ext import commands
import random

# Names of Roles in Game
# roles = ("L", "Kira", "Investigator")

# Creates a connection to the SQLite Database where the records are stored
con = sqlite3.connect('Database/games.db')
cur = con.cursor()

class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Function to check if the author is already entered in a record
    def check_inGame(self, ctx):
        check = cur.execute('SELECT * FROM players WHERE playerId = "{}"'
        .format(ctx.author.id))
        if check.fetchone():
            return True
        else:
            return False

# W.I.P (Incomplete)

    # Used to start a L's Game
    @commands.command()
    async def start(self, ctx):
        if self.check_inGame(ctx) is False:
            await ctx.reply('You are not in a L\'s Game')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = '{}'"
            .format(ctx.guild.id)).fetchone()[0]

            gamemaster_id = cur.execute("SELECT masterId FROM games WHERE guildId = '{}'"
            .format(ctx.guild.id)).fetchone()[0]

            gamemaster_user = self.bot.get_user(gamemaster_id)        

            if gamemaster_id != ctx.author.id:
                await ctx.reply('Only the Gamemaster: {} can start the game'
                .format(gamemaster_user.name))
            else:
                cur.execute("UPDATE games SET state = 'gameplay' WHERE guildId = '{}'"
                .format(ctx.guild.id))

                # Role Distribution
                play_data = cur.execute("SELECT * FROM players WHERE gameId = '{}'".format(g_id)).fetchall()
                players = []
                for i in range(len(play_data)):
                    players.append(play_data[i][0])
                cur.execute("UPDATE players SET role = '{}' WHERE gameId = '{}'".format("Investigator", g_id))

                # Assign Kira role to a random player
                choice = random.choice(players)
                cur.execute("UPDATE players SET role = '{}' WHERE gameId = '{}' AND playerId = '{}'".format("Kira", g_id, choice))
                players.remove(choice)

                # Assign L role to a random player
                choice = random.choice(players)
                cur.execute("UPDATE players SET role = '{}' WHERE gameId = '{}' AND playerId = '{}'".format("L", g_id, choice))
                players.remove(choice)

                con.commit()
        
def setup(bot):
    bot.add_cog(GameCog(bot))