import discord

class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        pass

    def setup(bot):
        bot.add_cog(SetupCog(bot))