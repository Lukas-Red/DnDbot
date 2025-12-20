import discord
from discord.ext import commands


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *args):
        await ctx.send(' '.join(args))

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))