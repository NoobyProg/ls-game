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
        check = cur.execute('SELECT * FROM players WHERE playerId = "{}"'
        .format(ctx.author.id))
        if check.fetchone():
            return True
        else:
            return False

    # Used to create a New L's Game
    @commands.command()
    async def create(self, ctx, g_channel : discord.TextChannel):
        check_guildGame = cur.execute("SELECT guildId FROM games WHERE guildId = '{}'"
        .format(ctx.guild.id)).fetchone()

        if self.check_inGame(ctx) == True:
            await ctx.send('You have already joined another game')
        elif check_guildGame:
            await ctx.send('An L\'s game is already ongoing in this server')
        else:
            # Adds the Author's data into the database
            cur.execute('INSERT INTO players (playerId, gameId) VALUES ("{}", "{}")'
            .format(ctx.author.id, game_id))
            cur.execute('INSERT INTO games (masterId, gameId, guildId, "state", channelId) VALUES ("{}", "{}", "{}", "pre-game", "{}")'
            .format(ctx.author.id, game_id, ctx.guild.id, g_channel.id))

            await ctx.send('An L\'s Game has been created with Game ID : **{}**'
            .format(game_id))

            con.commit()
    
    # Used to join an existing game
    @commands.command()
    async def join(self, ctx):
        if self.check_inGame(ctx) == True:
            await ctx.send('You have already joined another game')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = '{}'"
            .format(ctx.guild.id)).fetchone()[0]
            cur.execute('INSERT INTO players (playerId, gameId) VALUES ("{}", "{}")'
            .format(ctx.author.id, g_id))

            await ctx.send('Sucessfully joined L\'s Game with Game ID : **{}**'
            .format(g_id))

            con.commit()
        
    # Used to leave a joined L's Game
    @commands.command()
    async def leave(self, ctx):
        if self.check_inGame(ctx) == False:
            await ctx.send('You have not participated in an L\'s Game')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = '{}'"
            .format(ctx.guild.id)).fetchone()[0]
            cur.execute("DELETE FROM players WHERE playerId = '{}' AND gameId = '{}'"
            .format(ctx.author.id, g_id))

            await ctx.send('Sucessfully left L\'s Game with Game ID : **{}**'
            .format(g_id))

            con.commit()

# W.I.P (Incomplete)

    @commands.command()
    async def start(self, ctx):
        if self.check_inGame(ctx) == False:
            await ctx.send('You are not in a L\'s Game')
        else:
        
            gamemaster_id = cur.execute("SELECT masterId FROM games WHERE guildId = '{}'"
            .format(ctx.guild.id)).fetchone()[0]

            gamemaster_user = self.bot.get_user(gamemaster_id)
        
        
            if gamemaster_id != ctx.author.id:
                await ctx.send('Only the Gamemaster : {} can start the game'
                .format(gamemaster_user))
            else: 
                cur.execute("UPDATE games SET state = 'gameplay' WHERE guildId = '{}'"
                .format(ctx.guild.id))
        
def setup(bot):
    bot.add_cog(SetupCog(bot))