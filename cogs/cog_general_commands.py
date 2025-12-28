import discord
from discord.ext import commands

repo_url = "https://github.com/Lukas-Red/DnDbot"

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

    @commands.command()
    async def about(self, ctx):
        await ctx.send(f"Find the bot source here: {repo_url}")


async def setup(bot):
    await bot.add_cog(GeneralCommands(bot))