# Module Imports
from discord.ext import commands
import sqlite3
import random

# Names of Roles in Game
# roles = ("L", "Kira", "Investigator")

# Creates a connection to the SQLite Database where the records are stored
con = sqlite3.connect('Database/games.db')
con.row_factory = lambda cursor, row: row[0]
cur = con.cursor()

class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    anime_names = ['Inuyasha', 'Fai D. Flowright', 'Satashi', 'Amuro Ray', 'Momoko', 'Chibiusa', 'Masahiro', 'Rogue', 'Sora', 'Kouta', 'Roy', 'Riza', 'King Bradley', 'Ally', 'Tōtōsai', 'Kaede', 'Shirou Emiya', 'Takeshi Yamamoto', 'Koga', 'Kaname Tōsen', 'Airi', 'Launch', 'Hiroki', 'Mamoru', 'Banchi', 'Hoshi', 'Riku', 'Kyoya Hibari', 'Masuyo', 'Riko', 'Sasuke', 'Himawari', 'Pegasus Seiya', 'Bakkin', 'Lelouch Lamperouge', 'Hatori', 'Beerus', 'Hiroshi', 'Sakurako', 'Minako', 'Senku Ishigami', 'Kimi', 'Kohaku', 'Beyond the Grave', 'Luke fon Fabre', 'Absalom', 'Tohru', 'Erigor', 'Mizuki', 'Captain Harlock', 'Madoka', 'Yugi Mutou', 'Yasutora Sado', 'Yamcha', 'Madara Uchiha', 'Yori', 'Akira', 'Char Aznable', 'Kiyoshi', 'Sena Kobayakawa', 'Akumai', 'Edward Elric', 'Archer', 'An Zengaiina', 'Akihiro', 'Soifon', 'Hiro', 'Kazuhiro', 'Reiko', 'Jotaro Kujo', 'Kazuhiko', 'Havoc', 'Broly', 'Adele', 'Xellos', 'Kimiko', 'Nobu', 'Batchee', 'Kazuo', 'Shogo Makishima', 'Noboru', 'Gray', 'Seiji', 'Jun', 'Van Hohenheim', 'Setsuna F. Seiei', 'Phoenix Ikki', 'Kawaki', 'Mei', 'Kenichi', 'Banshee', 'Yoruichi', 'Itachi', 'Ume', 'Subaru Sumeragi', 'Temari', 'Albion', 'Taiki', 'Kaguya', 'Goku', 'Kaib', 'Belo Betty', 'Acilia', 'Tadashi', 'Strider Hiryu', 'Kotoko', 'Hotaru', 'Kokoro', 'Raditz', 'Bao Huang', 'Nephrite', 'Kenta', 'Midori', 'Wendy', 'Hideki', 'Daisuke', 'Tanjiro Kamado', 'Masumi', 'Arisa', 'Andromeda Shun', 'Bankuro', 'Tomiko', 'Miyuki']

    # Function to check if the author is already entered in a record
    def check_inGame(self, ctx):
        check = cur.execute('SELECT * FROM players WHERE playerId = ?'
        ,(ctx.author.id,))
        if check.fetchone():
            return True
        else:
            return False

    def players_list(self, ctx, g_id):
        players = cur.execute("SELECT playerId FROM players WHERE gameId = ?",(g_id,)).fetchall()
        return players
    
    def get_user_from_name(self, g_id, name):
        id = cur.execute('SELECT playerId FROM players WHERE name = ? AND gameId = ?', (name, g_id)).fetchone()
        user = self.bot.get_user(id)
        return user

    async def send_turn_message(self, user):
        await user.send("""
                **It is your turn in L's Game, what do you want to do?**

                1. Accusation - You can target a person with a strong intent.
                Usage : %accuse <name> <accusation text>

                2. Remark - You can pass a remark not targeted towards anyone but everyone.
                Usage : %remark <remark text>

                3. Pass - Pass this turn (Can only use this once per phase)
                Usage : %pass
                """)

# W.I.P (Incomplete)

    # Used to start a L's Game
    @commands.command()
    async def start(self, ctx):
        gamemaster_id = cur.execute("SELECT masterId FROM games WHERE guildId = ?"
            ,(ctx.guild.id,)).fetchone()

        gamemaster_user = self.bot.get_user(gamemaster_id)

        if self.check_inGame(ctx) is False:
            await ctx.reply('You are not in a L\'s Game')
        #elif cur.execute("SELECT state FROM games WHERE guildId = ?", (ctx.guild.id,)).fetchone() == "gameplay":
            #await ctx.reply('The game has already started')
        elif ctx.author != gamemaster_user:
            await ctx.reply('You are not the Gamemaster.')
        else:
            g_id = cur.execute("SELECT gameId FROM games WHERE guildId = ?",(ctx.guild.id,)).fetchone()    

            if gamemaster_id != ctx.author.id:
                await ctx.reply('Only the Gamemaster: ? can start the game'.format(gamemaster_user.name,))
            else:
                cur.execute("UPDATE games SET state = 'gameplay' WHERE guildId = ?",(ctx.guild.id,))

                #####################
                # ROLE DISTRIBUTION #
                #####################

                players_Role = self.players_list(ctx, g_id)

                # Assigns Names               
                random_names = random.sample(self.anime_names, len(players_Role))
                for i in players_Role:
                    cur.execute("UPDATE players SET name = ? WHERE playerId = ?",(random_names[players_Role.index(i)], i,))
                
                # Assign Investigator role to everyone (role will be changed for others later)
                cur.execute("UPDATE players SET role = ? WHERE gameId = ?",("Investigator", g_id,))

                # Assign Kira role to a random player
                Kira = random.choice(players_Role)
                cur.execute("UPDATE players SET role = ? WHERE gameId = ? AND playerId = ?",("Kira", g_id, Kira,))
                Kira_name = cur.execute('SELECT name FROM players WHERE role = ?', ("Kira",)).fetchone()                
                await self.bot.get_user(Kira).send(f"Welcome {Kira_name}.\nYou are **Kira**\nYour objective is to kill L by any means possible")
                players_Role.remove(Kira)

                # Assign L role to a random player
                L = random.choice(players_Role)
                cur.execute("UPDATE players SET role = ? WHERE gameId = ? AND playerId = ?",("L", g_id, L,))
                L_name = cur.execute('SELECT name FROM players WHERE role = ?', ("L",)).fetchone()
                await self.bot.get_user(L).send(f"Welcome {L_name}.\nYou are **L**.\nYou have to coordinate with the Task Force Investigators to reveal Kira's Identity.")
                players_Role.remove(L)

                # Information Phase
                # {0} = Kira, {1} = L, {2} = Investigator
                templates = ["Either {0} or {1} is Kira", "Either {1} or {0} is Kira", "Either {2} or {0} is Kira", "Either {0} or {2} is Kira", "Either {1} or {0} is L", "Either {0} or {1} is L", "Either {2} or {1} is L", "Either {1} or {2} is L", "{2} is also an investigator" * 3]

                for i in players_Role:
                    info_msg = random.choice(templates)
                    templates.remove(info_msg)

                    # TEMPORARY CONDITIONS FOR TESTING                    
                    if len(players_Role) < 3:
                        p1 = random.choice(players_Role)
                    else:
                        p1 = random.choice([x for x in players_Role if i != x])
                    p1_name = cur.execute("SELECT name FROM players WHERE playerId = ?", (p1,)).fetchone()

                    i_name = cur.execute("SELECT name FROM players WHERE playerId = ?",(i,)).fetchone()

                    await self.bot.get_user(i).send(f"Welcome {i_name}\nYou are an **Investigator**.\nYou know that " + info_msg.format("Placeholder", L_name, p1_name))

                del players_Role

                ##############
                # TURN ORDER #
                ##############

                players_Turn = self.players_list(ctx, g_id)
                for i in range(1,len(players_Turn)+1):
                    choice = random.choice(players_Turn)
                    cur.execute("UPDATE players SET turnOrder = ? WHERE gameId = ? AND playerId = ?",(i,g_id,choice,))
                    players_Turn.remove(choice)

                del players_Turn

                ##################
                # GAMEPLAY START #
                ##################
                names = cur.execute("SELECT name FROM players WHERE gameId = ?",(g_id,)).fetchall()
                g_channel = cur.execute("SELECT channelId FROM games WHERE guildId = ? AND gameId = ?",(ctx.guild.id, g_id,)).fetchone()
                g_channel = self.bot.get_channel(g_channel)

                cur.execute("UPDATE games SET round = ?, phase = ?, turnNo = ? WHERE guildId = ?", (1, 1, 1, ctx.guild.id))
                
                turns = cur.execute("SELECT turnOrder FROM players WHERE gameId = ?",(g_id,)).fetchall()
                players_ordered = [x for _,x in sorted(zip(turns, names), key=lambda pair: pair[0])]

                await g_channel.send("**The L's Game Begins**\n\nThe Players are :- \n" + "\n".join(players_ordered) + "\n")
                await g_channel.send(f"**PHASE 1 == ROUND 1 == TURN 1**")

                await self.send_turn_message(self.get_user_from_name(g_id, players_ordered[0]))
                
                con.commit()
    
    @commands.command()
    @commands.dm_only()
    async def remark(self, ctx, *, text):
        g_id = cur.execute("SELECT gameId FROM players WHERE playerId = ?",(ctx.author.id,)).fetchone()
        current_turn = cur.execute("SELECT turnNo FROM games WHERE gameId = ?", (g_id,)).fetchone()
        player_turn = cur.execute("SELECT turnOrder FROM players WHERE gameId = ? AND playerId = ?", (g_id, ctx.author.id,)).fetchone()
        g_channel = cur.execute("SELECT channelId FROM games WHERE gameId = ?",(g_id,)).fetchone()
        g_channel = self.bot.get_channel(g_channel)

        names = cur.execute("SELECT name FROM players WHERE gameId = ?",(g_id,)).fetchall()
        turns = cur.execute("SELECT turnOrder FROM players WHERE gameId = ?",(g_id,)).fetchall()
        players_ordered = [x for _,x in sorted(zip(turns, names), key=lambda pair: pair[0])]

        if self.check_inGame(ctx) is False:
            await ctx.reply("You are not in an L\'s Game")
        elif player_turn != current_turn:
            await ctx.reply("It is not your turn.")
        else:
            await g_channel.send(f"**TURN 1 | Remark | {players_ordered[current_turn - 1]}**\n{text}")
            await ctx.reply("Your Remark has been sent.")

                # W.I.P (Doesn't Work)
            # if current_turn == len(players_ordered):
            #     round_count = cur.execute("SELECT round FROM games WHERE gameId = ?",(g_id,)).fetchone()
            #     if round_count == 3:
            #         phase_count = cur.execute("SELECT phase FROM games WHERE gameId = ?",(g_id,)).fetchone()
            #         if phase_count == 3:
            #             await g_channel.send("Iske aage code nahi kiya")
            #         else:
            #             cur.execute("UPDATE games SET turnNo = ?, round = ?, phase = ? WHERE gameId = ?", (1, 1, phase_count + 1, g_id,))
            #             await self.send_turn_message(self.get_user_from_name(g_id, players_ordered[current_turn]))
                
            #     else:
            #         cur.execute("UPDATE games SET turnNo = ?, round = ? WHERE gameId = ?", (1, round_count + 1, g_id,))
            #         await self.send_turn_message(self.get_user_from_name(g_id, players_ordered[current_turn]))
            
            # else:
            cur.execute("UPDATE games SET turnNo = ? WHERE gameId = ?", (current_turn + 1, g_id,))

            await self.send_turn_message(self.get_user_from_name(g_id, players_ordered[current_turn]))
        
        con.commit()

def setup(bot):
    bot.add_cog(GameCog(bot))