
import logging
import discord
from discord.ext import commands
import config
from db import db_initialize
from cogs.economy import setup
from cogs.features import feature_setup

intents=discord.Intents.default()
intents.message_content=True
intents.members=True

bot=commands.Bot(command_prefix=config.PREFIX, intents=intents)

setup(bot)
feature_setup(bot)

@bot.event
async def on_ready():
    db_initialize()
    print(f"Berry Broker Ledger online. Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        await member.send(f"Welcome to the Grand Line, rookie {member.name}")
    except discord.Forbidden:
        pass


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(config.TOKEN)