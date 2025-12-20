import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

token = open('.bot_token', 'r').read().strip()

bot.run(token)