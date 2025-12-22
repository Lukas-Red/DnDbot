import modnar
import discord
from discord.ext import commands


class ModnarCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.modnar_staff = modnar.Modnar()

    @commands.command()
    async def modnar(self, ctx):
        modnar_spell = self.modnar_staff.get_modnar_spell_embed()
        if isinstance(modnar_spell, discord.Embed):
            await ctx.send(embed=modnar_spell)
        else:
            await ctx.send(modnar_spell)
    
    @commands.command()
    @commands.is_owner()
    async def modnar_get_distribution(self, ctx):
        await ctx.send(self.modnar_staff.get_stats())
    
    @commands.command()
    @commands.is_owner()
    async def modnar_set_distribution(self, ctx, *args):
        arg = ''.join(args)
        await ctx.send(self.modnar_staff.set_distribution(arg))
    
    @commands.command()
    @commands.is_owner()
    async def modnar_write_distribution(self, ctx):
        await ctx.send(self.modnar_staff.write_distribution())

async def setup(bot):
    await bot.add_cog(ModnarCommands(bot))