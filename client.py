# client.py
import os
import discord
from discord import Embed
from dotenv import load_dotenv
from discord.ext import commands
from bot import getInfo

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
client = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='price', help="Search for price of game based on URL or keyword search.")
async def price(ctx, *args):
    query = " ".join(args)
    msg = getInfo(query)
    if msg == None:
        await ctx.send(f"Sorry, there are no results for '{query}'. Please try again.")
        return 0

    print(msg)

    response = Embed(title=msg['url'].split("/")[5], description=msg['url'], color=0x347aeb)

    for key, val in msg.items():
        if key == 'dlc':
            text = ""
            for opt, prices in val.items():
                text += f"{opt}:\n"
                if prices == '':
                    continue
                for price_type, price in prices.items():
                    if price == '':
                        continue
                    text += f"```\t- {price_type}: {price}```\n"
            print(text)
                
            response.add_field(name="DLCs", value=text, inline=False)
        elif key == 'game_options':
            text = ""
            for opt, prices in val.items():
                text += f"{opt}:\n"
                if prices == '':
                    continue
                for price_type, price in prices.items():
                    if price == '':
                        continue
                    text += f"```\t- {price_type}: {price}```\n"
            print (text)
            response.add_field(name="Purchase Options", value=text, inline=False)

    await ctx.send(embed=response)

@bot.command(name='sale', help="Check if a game is on sale.")
async def sale(ctx, *args):
    query = " ".join(args)
    msg = getInfo(query)
    game_title = msg['url'].split("/")[5]
    if msg == None:
        await ctx.send(f"Sorry, there are no results for '{query}'. Please try again.")
        return 0

    discount = False
    response = f"```{game_title} has the following sales:\n"
    for k in msg.keys():
        if k == 'game_options' or k == 'dlc':
            if msg[k] == '':
                continue
            for game in msg[k].keys():
                if msg[k][game] == '':
                    continue
                if 'Discount' in msg[k][game].keys():
                    if msg[k][game]['Discount'] == '':
                        continue
                    response += f"\t{game}: {msg[k][game]['Discount']} off\n"
                    discount = True
    if discount == True:
        response += "```" 
    else:
        response = f"There are currently no sales on {game_title}. Check again later!"
    
    await ctx.send(response)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    copy = f"{message.author.mention} in "
    if isinstance(message.channel, discord.channel.DMChannel):
        copy += "DM: "
    elif isinstance(message.channel, discord.channel.TextChannel):
        copy += f"#{message.channel.name}: "
    else:
        print("other type of channel")
        return

    copy += f"<br> ```{message.content}```"
    print(copy)
    carol = await bot.fetch_user(549436545019674626)
    await carol.send(copy)

bot.run(TOKEN)