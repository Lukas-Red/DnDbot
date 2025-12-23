import dice_roller
import discord
from discord.ext import commands


class RollCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *args):
        print(len(args))
        print(args)
        await ctx.send(dice_roller.handle_roll_query(args))
    

async def setup(bot):
    await bot.add_cog(RollCommands(bot))