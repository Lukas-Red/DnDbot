import discord
from discord.ext import commands

import spell_parser

class SpellCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spellbook = spell_parser.SpellBook('5etools-src/data/spells/spells-xphb.json')


    @commands.command()
    async def spell(self, ctx, *args):
        arg = ' '.join(args)
        spell_info = self.spellbook.get_spell(arg)
        await ctx.send(spell_info)


async def setup(bot):
    await bot.add_cog(SpellCommands(bot))