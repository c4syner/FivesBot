"""
Currently this is executed via a discord async loop:
However it silently crashes after a few days;
Will move to discord webhooks
"""

from util import opensea
from datetime import datetime
from discord.ext import commands
from discord.ext.tasks import loop

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


import requests

import discord

import copy


API = "2d5ca92fcfe849389a0cf12b73df9340"
CONTRACT = "0x017Ba9AC7916ebd646e7c11DD220c05c5b790224"
BOT_ID = ""

intents = discord.Intents.none()
intents.reactions = True
intents.members = True
intents.guilds = True


os = opensea.OpenSea(ETH_CONTRACT=CONTRACT, API_KEY=API)
bot = commands.Bot(command_prefix='a.', intents=intents)
past_data = []
channels = [885935079791161415, 891002883863097345]
gas_channel = 893010436948111361
initState = 0
iter1 = 0
elapsed = 0
@loop(seconds=1)
async def os_watch():
    await bot.wait_until_ready()
    global past_data
    global iter1
    global initState
    iter1 += 1
    print(iter1)
    #channel = bot.get_channel()  # replace with channel ID that you want to send to
    try:
        sales = os.get_recent_sales()
    except:
        print("OpenSea API error")
        return 0
    if(initState == 0):
        initState = 1
        past_data = copy.copy(sales)

    if(past_data == []):
        past_data = copy.copy(sales)

    pendingData = []
    for item in sales:
        validate = True
        for past_item in past_data:
            if(item[0] == past_item[0]):
                validate = False
        if(validate):
            pendingData.append(item)

    for item in pendingData:
        #send these mfs to the trenches
        for dp in channels:

            channel = bot.get_channel(dp)

            svg_source = requests.get(item[6]).text
            print(svg_source)
            with open('sales.svg', 'w') as file:
                file.write(svg_source)

            drawing = svg2rlg("sales.svg")
            renderPM.drawToFile(drawing, "sales.png", fmt="PNG")

            file = discord.File("sales.png")

            payload = "[OpenSea Link]"+ "(https://opensea.io/assets/" + CONTRACT + "/" + item[1] + ")"
            embedVar = discord.Embed(title="Fives #" + str(item[1]) + " purchased for " + str(item[2]) + " ETH | $" + str(item[3]), description=payload, color=0xFF0000)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            embedVar.set_image(url="attachment://sales.png")
            await channel.send(embed=embedVar, file=file)



    past_data = sales



os_watch.start()

@bot.command()
async def info(ctx):
    await bot.wait_until_ready()
    print("11111")
    payload = "**About**\n\nHere you can get pinged whenever the Ethereum gas price drops below 50 gwei.\n`.add` to give yourself the role to be pinged whenever gas is low.\n`.remove` to remove the role to be pinged."
    embedVar = discord.Embed(description=payload, color=0xFF0000)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))
    await ctx.message.channel.send(embed=embedVar)

bot.run(BOT_ID)