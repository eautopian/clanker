import discord
import datetime

SUCCESS_COLOUR = discord.Color.blurple()
BAD_COLOUR = discord.Color.red()

if datetime.datetime.now().month == 10:
    SUCCESS_COLOUR = discord.Color.orange()
    BAD_COLOUR = discord.Color.purple()
elif datetime.datetime.now().month == 12:
    SUCCESS_COLOUR = discord.Color.green()
    BAD_COLOUR = discord.Color.red()
elif datetime.datetime.now().month == 3:
    SUCCESS_COLOUR = discord.Color.green()
    BAD_COLOUR = discord.Color.pink()