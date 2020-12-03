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
    
    carol = await bot.fetch_user(549436545019674626)

    copy = f"{message.author.mention} in "

    # If DM message...
    if isinstance(message.channel, discord.channel.DMChannel):
        # If message is from carol, relay message to specified channel if valid
        if (message.author == carol):
            print("user is carol")
            # If message doesn't have a space-separated channel name, invalid
            if len(message.content.split(" ", 1)) < 2:
                print(f"Invalid message")
                return

            target_channel = None
            # Get channel by specified channel name (first space-separated word)
            channel_name = message.content.split(" ", 1)[0]
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == channel_name:
                        target_channel = channel
                        break

            # If channel doesn't exist, tell user and return
            if not target_channel:
                print(f"Invalid channel: {channel_name}")
                await carol.send(f"Invalid channel: {channel_name}")
                return
            
            # Send message (everything after first space)
            print(f"Sending message: {message.content.split(' ', 1)[1]}")
            await target_channel.send(message.content.split(" ", 1)[1])
            return

        # Else, this is a DM from someone else
        else:
            copy += "DM: "
    
    # If text channel, add channel name to copy
    elif isinstance(message.channel, discord.channel.TextChannel):
        copy += f"#{message.channel.name}: "

    # Else, log that this is a different channel type
    else:
        print("other type of channel")
        return

    # Add message content to copy and send to carol
    copy += f"```{message.content}```"
    print(copy)
    await carol.send(copy)

bot.run(TOKEN)