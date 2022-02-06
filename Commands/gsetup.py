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

    # Function to check if the author is already entered in a record
    def check_inGame(self, ctx):
        check = cur.execute('SELECT * FROM players WHERE playerId = ?', (ctx.author.id,))
        if check.fetchone():
            return True
        else:
            return False

    # Used to create a New L's Game
    @commands.command()
    async def create(self, ctx, g_channel : discord.TextChannel):
        check_guildGame = cur.execute("SELECT guildId FROM games WHERE guildId = ?",(ctx.guild.id,)).fetchone()

        if self.check_inGame(ctx) is True:
            await ctx.reply('You have already joined another game')
        elif check_guildGame:
            await ctx.reply('A L\'s game is already ongoing in this server')
        else:
            # Adds the Command User's data into the database
            cur.execute('INSERT INTO players(playerId, gameId) VALUES(?, ?)'
            ,(ctx.author.id, game_id,))
            cur.execute('INSERT INTO games(masterId, gameId, guildId, "state", channelId, turnNo, round, phase) VALUES(?, ?, ?, "pre-game", ?, 0, 0, 0)'
            ,(ctx.author.id, game_id, ctx.guild.id, g_channel.id,))

            await ctx.reply('A L\'s Game has been created with Game ID : **{}**'.format(game_id))

            con.commit()
    
    # Used to join an existing L's game
    @commands.command()
    async def join(self, ctx):
        if self.check_inGame(ctx) is True:
            await ctx.reply('You have already joined another game')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = ?"
            ,(ctx.guild.id,)).fetchone()[0]
            cur.execute('INSERT INTO players (playerId, gameId) VALUES (?, ?)'
            ,(ctx.author.id, g_id,))

            await ctx.reply('Sucessfully joined L\'s Game with Game ID : **{}**'
            .format(g_id))

            con.commit()
        
    # Used to leave a joined L's Game
    @commands.command()
    async def leave(self, ctx):
        if self.check_inGame(ctx) is False:
            await ctx.reply('You have not participated in a L\'s Game')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = ?"
            ,(ctx.guild.id,)).fetchone()[0]
            cur.execute("DELETE FROM players WHERE playerId = ? AND gameId = ?"
            ,(ctx.author.id, g_id,))

            await ctx.reply('Sucessfully left L\'s Game with Game ID : **{}**'.format(g_id,))

            # W.I.P to check if game has no players and Delete the Game
            """
            play_g_id = cur.execute("SELECT gameId FROM games WHERE EXISTS (SELECT gameId FROM players WHERE players.gameId = games.gameId)")
            if play_g_id == None:
                cur.execute("DELETE FROM games WHERE gameId = ?"
                ,(g_id))
                await ctx.send("No Players found in game : ?\nDeleting the game",(g_id,))

            
            """
            con.commit()
        
def setup(bot):
    bot.add_cog(SetupCog(bot))