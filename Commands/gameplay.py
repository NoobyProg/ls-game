# Module Imports
import discord
import sqlite3
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup

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

    def players_list(self, ctx):
        g_id = cur.execute("SELECT gameId FROM games WHERE guildId = '{}'"
            .format(ctx.guild.id)).fetchone()[0]
        play_data = cur.execute("SELECT playerId FROM players WHERE gameId = '{}'".format(g_id)).fetchall()
        players = []
        for i in range(len(play_data)):
            players.append(play_data[i][0])
        return players

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

                #####################
                # ROLE DISTRIBUTION #
                #####################

                players = self.players_list(ctx)

                # Assign Investigator role to everyone (roll will be changed for others later)
                cur.execute("UPDATE players SET role = '{}' WHERE gameId = '{}'".format("Investigator", g_id))

                """"
                # Assign Kira role to a random player
                Kira = random.choice(players)
                cur.execute("UPDATE players SET role = '{}' WHERE gameId = '{}' AND playerId = '{}'".format("Kira", g_id, Kira))
                await self.bot.get_user(Kira).send("You are Kira")
                players.remove(Kira)
                """

                # Assign L role to a random player
                L = random.choice(players)
                cur.execute("UPDATE players SET role = '{}' WHERE gameId = '{}' AND playerId = '{}'".format("L", g_id, L))
                await self.bot.get_user(L).send("You are L")
                players.remove(L)

                # Information Phase
                templates = ("Either `#` or `@` is L","`#` is also an Investigator")
                name_page = requests.get("https://www.generatormix.com/random-anime-character-generator")

                soup = BeautifulSoup(name_page.content, 'html.parser')
                results = soup.find(id='output')
                name_elements = results.find_all('h3', class_='text-center')

                for i in players:
                    temp = random.choice(templates)
                    if "@" in temp:
                        x = temp.replace("@", self.bot.get_user(L).name)
                        x = x.replace("#", self.bot.get_user(random.choice(players)).name)
                    else:
                        x = temp.replace("#", self.bot.get_user(random.choice(players)).name)
                    await self.bot.get_user(i).send("You are an Investigator\nYou know that {}".format(x))

                del players

                ##############
                # TURN ORDER #
                ##############

                players = self.players_list(ctx)
                for i in range(1,len(players)+1):
                    choice = random.choice(players)
                    cur.execute("UPDATE players SET turnOrder = {} WHERE gameId = '{}' AND playerId = '{}'".format(i,g_id,choice))
                    players.remove(choice)

                ##################
                # GAMEPLAY START #
                ##################

                

                con.commit()
        
def setup(bot):
    bot.add_cog(GameCog(bot))