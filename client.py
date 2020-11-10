# client.py
import os
import random
from discord import Embed
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
    msg = getInfo(query)
    if msg == None:
        await ctx.send(f"Sorry, there are no results for '{query}'. Please try again.")
        return 0

    response = Embed(title="Game Name", description=msg['url'], color=0x00ff00)
    for key, val in msg:
        if key == 'dlc':
            response.add_field(name="DLCs", value="", inline=False)
    response.add_field(name="Field1", value="hi", inline=False)
    response.add_field(name="Field2", value="hi2", inline=False)
  
    msg = getInfo(query)

    await ctx.send(embed=response)

bot.run(TOKEN)