import discord
from discord.ext import commands

import spell_parser

class SpellCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spellbook = spell_parser.get_instance("spellbook")


    @commands.command()
    async def spell(self, ctx, *args):
        arg = ' '.join(args)
        spell_info = self.spellbook.get_spell_embed_dict(arg)
        if isinstance(spell_info, discord.Embed):
            await ctx.send(embed=spell_info)
        else:
            await ctx.send(spell_info)  


async def setup(bot):
    await bot.add_cog(SpellCommands(bot))