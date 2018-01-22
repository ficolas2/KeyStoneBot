#Discord bot running python3 using Discord.py
#
#API reference and documentation:
#http://discordpy.readthedocs.io/en/rewrite/api.html
#https://github.com/Rapptz/discord.py/tree/rewrite/examples
#
#Other useful links:
#https://leovoel.github.io/embed-visualizer/

#TODO - make messages beautiful with the visualizer
#TODO - implement error feedback and information when commands error
#TODO - make everything work


import discord
from discord.ext import commands
import random

import os

import time
import datetime
from datetime import datetime, date
from datetime import timedelta

import subprocess

import sys

import unitconversion

description = '''A moderator assisting bot created for KeyStoneScience\'s server.'''
bot = commands.Bot(command_prefix='!', description=description)

starttime = datetime.now()
longprefix = ':strawberry: PiPy KeyStoneBot | '
shortprefix = ':strawberry: '

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.group()
async def clean(ctx):
    """Cleans messages in the channel the command is typed in."""
    if ctx.invoked_subcommand is None:
        await ctx.send(shortprefix + 'Possible subcommands are \'user\' or \'any\'.')

@clean.command(name='user')
async def _user(ctx, member: discord.Member):
    """Cleans messages from [user] in the channel the command is typed in."""
    deleted = await ctx.channel.purge(limit=100, check=lambda x: x.author == member)
    tmp = await message.channel.send(longprefix + 'Cleaning\nDeleted {} message(s) from {}'.format(len(deleted), member))
    await asyncio.sleep(5.0)
    await tmp.delete()

@clean.command(name='any')
async def _any(ctx, amount: int):
    """Cleans the last [n] messages in the channel the command is typed in. If no argument is given, it removes the last 10 messages."""
    await ctx.send(shortprefix + 'you wanted to delete {0} messages.'.format(amount))
    if amount > 0 and amount < 301:
        deleted = await message.channel.purge(limit=amount)
    else:
        deleted = await message.channel.purge(limit=10)
        tmp = await message.channel.send(longprefix + 'Cleaning\nDeleted {} message(s)'.format(len(deleted)))
        await asyncio.sleep(5.0)
        await tmp.delete()

@bot.command()
async def temperature(ctx):
    """Shows the system core temperature of the host system this bot is running on."""
    result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    await message.channel.send(longprefix + 'Temperature\n```%s```' % (result.stdout[0:-1].decode('ascii')))

@bot.command()
async def about(ctx):
    """Shows information about the bot aswell as the relevant version numbers."""
    await ctx.send(longprefix + 'Info\n*PiPy KeyStoneBot is a Discord bot created by <@378840449152188419> to enhance the moderator\'s efficiency in KeyStoneScience\'s server. Hosted on a Raspberry PI 3, running inside Raspberian on Python using Discord.py.*\n\nPiPy KeyStoneBot version: `%s`\nDiscord.py version: `%s`\nPython version: `%s`' % (date.fromtimestamp(os.path.getmtime('/home/pi/FTP/keystonebot.py')), discord.__version__, sys.version.split(' ')[0]))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member has joined the server."""
    await ctx.send(shortprefix + '{0.name} has joined on {0.joined_at}.'.format(member))

@bot.event
async def on_message(message):
    if bot.user.id is not message.author.id:
        processedMessage = unitconversion.process(message.content)
        if processedMessage is not None:
            correctionText = "I think " + message.author.name + " meant to say: ```" + processedMessage + "```Please forgive him."
            await message.channel.send(correctionText)

with open('token', 'r') as content_file:
    content = content_file.read()

bot.run(content)
