import discord
from discord.ext import commands
import asyncio
import os

import spell_parser


bot_token = open('.bot_token', 'r').read().strip()
cog__file_prefix = 'cog_'
prefix = '!'


intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intent)

async def load_cogs():
    for filename in os.listdir('.'):
        if filename.startswith(cog__file_prefix) and filename.endswith('.py'):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(cog_name)
                print(f'Loaded cog: {cog_name}')
            except Exception as e:
                print(f'Critical failure: unable to load cog {cog_name}')
                print(f'Error: {e}')
                exit(1)

@bot.event
async def on_ready():
    print(f'{bot.user} is now online!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("Insufficient privilege for this command: owner only.")
        return

    if isinstance(error, commands.CommandNotFound):
        await ctx.send("No such command. Try !help")
        return
    
    raise error


async def main():
    async with bot:
        await load_cogs()
        await bot.start(bot_token)

if __name__ == '__main__':
    asyncio.run(main())