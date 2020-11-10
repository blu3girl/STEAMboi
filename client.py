# client.py
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from bot import getInfo

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='price', help="Search for price of game based on URL or keyword search.")
async def price(ctx, query):    
    response = getInfo(query)
    if response == None:
        response = f"Sorry, there are no results for '{query}'. Please try again.'"
    print(response)
    await ctx.send(response)

bot.run(TOKEN)
