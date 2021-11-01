 #v1 FIVES Stats
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

import discord
from discord.ext import menus

import math
import copy
import time
import random
import statistics

import fives_data

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import requests
import opensea

import matplotlib.pyplot as plt
import os

class RarityPages(menus.Menu):
    async def send_initial_message(self, ctx, channel):

        payload = copy.copy(self.embed_var.description)
        this_embed = copy.copy(self.embed_var)


        pages = math.ceil(len(self.data) / 10)

        dat = "```\n"
        for i in range(len(self.data)):
            if(i >= self.iter_var and i < self.iter_cap+self.iter_var):
                dat = dat + str(self.data[i]) + "\n"
        dat = dat + "```"
        payload = payload + dat
        this_embed.description = payload

        this_embed._footer["text"] = "Project Fives • Page " + str(int(1)) + " of " + str(pages)

        return await channel.send(embed=this_embed)

    @menus.button('◀')
    async def on_back(self, payload):
        self.iter_var = self.iter_var - 10
        if(self.iter_var < 0):
            self.iter_var = 0

        pages = math.ceil(len(self.data) / 10)
        if (self.iter_var != 0):
            this_page = 1 + (self.iter_var / 10)
        else:
            this_page = 1



        payload = copy.copy(self.embed_var.description)
        this_embed = copy.copy(self.embed_var)

        dat = "```\n"
        for i in range(len(self.data)):
            if (i >= self.iter_var and i < self.iter_cap + self.iter_var):
                dat = dat + str(self.data[i]) + "\n"
        dat = dat + "```"
        payload = payload + dat
        this_embed.description = payload

        if (this_page == pages):
            self.iter_var = self.iter_var - 10

        this_embed._footer["text"] = "Project Fives • Page " + str(int(this_page)) + " of " + str(pages)

        await self.message.edit(embed=this_embed)

    @menus.button('▶')
    async def on_right(self, payload):
        pages = math.ceil(len(self.data) / 10)
        #little test for overflow
        if (self.iter_var != 0):
            this_page = 1 + (self.iter_var / 10)
        else:
            this_page = 1

        if(this_page == pages):
            self.iter_var = self.iter_var - 10

        self.iter_var = self.iter_var + 10
        if (self.iter_var > len(self.data)):
            self.iter_var = len(self.data)-10

        if (self.iter_var != 0):
            this_page = 1 + (self.iter_var / 10)
        else:
            this_page = 1




        payload = copy.copy(self.embed_var.description)
        this_embed = copy.copy(self.embed_var)


        dat = "```\n"
        for i in range(len(self.data)):
            if (i >= self.iter_var and i < self.iter_cap + self.iter_var):
                dat = dat + str(self.data[i]) + "\n"
        dat = dat + "```"
        payload = payload + dat
        this_embed.description = payload

        this_embed._footer["text"] = "Project Fives • Page " + str(int(this_page)) + " of " + str(pages)

        await self.message.edit(embed=this_embed)

class OSPages(menus.Menu):
    async def send_initial_message(self, ctx, channel):

        payload = copy.copy(self.embed_var.description)
        this_embed = copy.copy(self.embed_var)


        pages = math.ceil(len(self.data) / 10)

        dat = "\n\n**Matching Listings:**\n"
        for i in range(len(self.data)):
            if(i >= self.iter_var and i < self.iter_cap+self.iter_var):
                dat = dat + "[" + str(self.data[i]["token_id"]) + "](https://opensea.io/assets/0x017ba9ac7916ebd646e7c11dd220c05c5b790224/" + str(self.data[i]["token_id"]) + ")" + " - **" + str(self.data[i]["eth_price"]) + " ETH | $" + str(round(self.data[i]["eth_price"] * self.data[i]["usd_eth_rate"], 2)) + "**\n"

        payload = payload + dat
        this_embed.description = payload

        this_embed._footer["text"] = "Project Fives • Page " + str(int(1)) + " of " + str(pages)

        return await channel.send(embed=this_embed)

    @menus.button('◀')
    async def on_back(self, payload):
        self.iter_var = self.iter_var - 10
        if(self.iter_var < 0):
            self.iter_var = 0

        pages = math.ceil(len(self.data) / 10)
        if (self.iter_var != 0):
            this_page = 1 + (self.iter_var / 10)
        else:
            this_page = 1



        payload = copy.copy(self.embed_var.description)
        this_embed = copy.copy(self.embed_var)
        dat = "\n\n**Matching Listings:**\n"
        for i in range(len(self.data)):
            if (i >= self.iter_var and i < self.iter_cap + self.iter_var):
                dat = dat + "[" + str(self.data[i]["token_id"]) + "](https://opensea.io/assets/0x017ba9ac7916ebd646e7c11dd220c05c5b790224/" + str(self.data[i]["token_id"]) + ")" + " - **" + str(self.data[i]["eth_price"]) + " ETH | $" + str(round(self.data[i]["eth_price"] * self.data[i]["usd_eth_rate"], 2)) + "**\n"

        payload = payload + dat
        this_embed.description = payload

        if (this_page == pages):
            self.iter_var = self.iter_var - 10

        this_embed._footer["text"] = "Project Fives • Page " + str(int(this_page)) + " of " + str(pages)

        await self.message.edit(embed=this_embed)

    @menus.button('▶')
    async def on_right(self, payload):
        pages = math.ceil(len(self.data) / 10)
        #little test for overflow
        if (self.iter_var != 0):
            this_page = 1 + (self.iter_var / 10)
        else:
            this_page = 1

        if(this_page == pages):
            self.iter_var = self.iter_var - 10

        self.iter_var = self.iter_var + 10
        if (self.iter_var > len(self.data)):
            self.iter_var = len(self.data)-10

        if (self.iter_var != 0):
            this_page = 1 + (self.iter_var / 10)
        else:
            this_page = 1



        payload = copy.copy(self.embed_var.description)
        this_embed = copy.copy(self.embed_var)
        dat = "\n\n**Matching Listings:**\n"
        for i in range(len(self.data)):
            if (i >= self.iter_var and i < self.iter_cap + self.iter_var):
                dat = dat + "[" + str(self.data[i]["token_id"]) + "](https://opensea.io/assets/0x017ba9ac7916ebd646e7c11dd220c05c5b790224/" + str(self.data[i]["token_id"]) + ")" + " - **" + str(self.data[i]["eth_price"]) + " ETH | $" + str(round(self.data[i]["eth_price"] * self.data[i]["usd_eth_rate"], 2)) + "**\n"

        payload = payload + dat
        this_embed.description = payload

        this_embed._footer["text"] = "Project Fives • Page " + str(int(this_page)) + " of " + str(pages)

        await self.message.edit(embed=this_embed)



bot = commands.Bot(command_prefix=['f.','F.'], help_command=None)
COLOR = 0xff0000
datalink = fives_data.FivesData()

API = "2d5ca92fcfe849389a0cf12b73df9340"
CONTRACT = "0x017Ba9AC7916ebd646e7c11DD220c05c5b790224"

oss = opensea.OpenSea(ETH_CONTRACT=CONTRACT, API_KEY=API)



@bot.command()
async def rarity(ctx):
    plist = []
    players = ctx.message.content.replace("f.rarity ", "").upper()
    if ("," in players):
        # parse multiple players
        players = players.split(",")
        for i in range(len(players)):
            # remove extraneous white space
            temp_p = list(players[i])
            if (temp_p[0] == " "):
                temp_p = temp_p[1:]
            if (temp_p[-1] == " "):
                temp_p = temp_p[:-1]
            true_p = "".join(temp_p)
            plist.append(true_p)
    else:
        plist.append(players)
    if(len(plist) == 2 and plist[0] == plist[1]): #check doubles
        match_ids = []
        count = 0
        for i in range(len(datalink.player_by_id)):
            validate = False

            this_p = datalink.player_by_id[i]
            if(plist[0] == this_p[2] and plist[0] == this_p[3]):
                validate=True
            elif(plist[0] == this_p[4] and plist[0] == this_p[5]):
                validate=True

            if (validate):
                count += 1
                match_ids.append(str((datalink.player_by_id[i][0])))
    else:

        match_ids = []
        count = 0
        for i in range(len(datalink.player_by_id)):
            validate = True
            for j in plist:
                if (j not in datalink.player_by_id[i]):
                    validate = False
                    break
            if (validate):
                count += 1
                match_ids.append(str((datalink.player_by_id[i][0])))


    if (count == 0):
        pstr = " + ".join(plist)
        payload = "No matches for **" + pstr + "**"
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
        return None

    percent = round((count / 8000) * 100, 4)
    pstr = " + ".join(plist)
    payload = "**" + pstr + ":**\n" + "# of Drops: **" + str(count) + "**\nDrop Rate: **" + str(percent) + "%**"
    payload = payload + "\n\n**Matching Teams:**"
    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project Fives"))

    m = RarityPages()
    await m.start(ctx, embed_var=embedVar, data=match_ids)

@bot.command()
async def gasph(ctx):
    resp = requests.get("https://ethgasapi.c4syner.repl.co/gas_hour.json").json()
    parse = resp["maps"]
    gaspoints = []
    for item in parse:
        gaspoints.append(item["gas"]["avg"])
    plt.style.use('dark_background')
    plt.title("Gas Hourly")
    plt.ylabel('Gas (gwei)')
    plt.xlabel("Gas x minutes ago")

    plt.plot(gaspoints,color="#ff0000", label="Gas Price")
    plt.gca().set_xticklabels([70,60,50,40,30,20,10,0])

    plt.legend()
    imf ="five_img"+str(random.randint(1,10000))+'.png'
    plt.savefig(imf)
    plt.clf()

    file = discord.File(imf)
    embedVar = discord.Embed(color=COLOR)
    embedVar.set_image(url="attachment://" + imf)

    await ctx.message.channel.send(embed=embedVar, file=file)
    os.remove(imf)


@bot.command()
async def orderbook(ctx):
    plist = []
    players = ctx.message.content.replace("f.orderbook ", "").upper()
    if ("," in players):
        # parse multiple players
        players = players.split(",")
        for i in range(len(players)):
            # remove extraneous white space
            temp_p = list(players[i])
            if (temp_p[0] == " "):
                temp_p = temp_p[1:]
            if (temp_p[-1] == " "):
                temp_p = temp_p[:-1]
            true_p = "".join(temp_p)
            plist.append(true_p)
    else:
        plist.append(players)
    if (len(plist) == 2 and plist[0] == plist[1]):  # check doubles
        match_ids = []
        count = 0
        for i in range(len(datalink.player_by_id)):
            validate = False

            this_p = datalink.player_by_id[i]
            if (plist[0] == this_p[2] and plist[0] == this_p[3]):
                validate = True
            elif (plist[0] == this_p[4] and plist[0] == this_p[5]):
                validate = True

            if (validate):
                count += 1
                match_ids.append(str((datalink.player_by_id[i][0])))
    else:

        match_ids = []
        count = 0
        for i in range(len(datalink.player_by_id)):
            validate = True
            for j in plist:
                if (j not in datalink.player_by_id[i]):
                    validate = False
                    break
            if (validate):
                count += 1
                match_ids.append(str((datalink.player_by_id[i][0])))

    if (count == 0):
        pstr = " + ".join(plist)
        if (pstr == "F.ORDERBOOK"):
            payload = "No players supplied."
        else:
            payload = "No matches for **" + pstr + "**"
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
        return None

    resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
    renderStack = []
    for j in range(len(resp["data"])):
        if (resp["data"][j]["token_id"] in match_ids):
            renderStack.append(resp["data"][j]["eth_price"])

    if (renderStack == []):
        # none listed
        pstr = " + ".join(plist)
        payload = "No listings on OpenSea for **" + pstr + "**"
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
        return None
    pstr = " + ".join(plist)

    #Create orderbook image

    plt.style.use('dark_background')
    plt.title(pstr + " Orderbook")
    plt.ylabel('Ether')
    plt.xlabel('#of Orders')

    renderStack.sort()
    x = []
    y = []
    q1 = statistics.median(renderStack[:math.floor((len(renderStack)/2))])
    q3 = statistics.median(renderStack[(math.floor(len(renderStack)/2)):])
    iqr = q3-q1
    top = q3+(1.5*iqr)

    for l in range(len(renderStack)):
        if(renderStack[l] <= top):

            y.append(renderStack[l])
            x.append(l)


    plt.step(x,y,color="#ff0000", label="Liquidity")
    plt.fill_between(x,y, color="#ff0000", step="pre", alpha=0.4)
    plt.legend()
    imf ="five_img"+str(random.randint(1,10000))+'.png'
    plt.savefig(imf)
    plt.clf()

    file = discord.File(imf)
    embedVar = discord.Embed(color=COLOR)
    embedVar.set_image(url="attachment://" + imf)

    await ctx.message.channel.send(embed=embedVar, file=file)
    os.remove(imf)



@bot.command()
async def florderbook(ctx):
    id = int(ctx.message.content.split(" ")[1])
    match_ids = []
    for i in range(len(datalink.rarity_breakdown_extra)):
        if(datalink.rarity_breakdown_extra[i][-1] == id):
            match_ids.append(datalink.rarity_breakdown_extra[i][0])


    resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
    renderStack = []
    for j in range(len(resp["data"])):
        if (int(resp["data"][j]["token_id"]) in match_ids):
            renderStack.append(resp["data"][j]["eth_price"])

    if (renderStack == []):
        # none listed
        payload = "No listings on OpenSea."
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
        return None


    #Create orderbook image

    plt.style.use('dark_background')
    plt.title(str(id) + " Red" + " Orderbook")
    plt.ylabel('Ether')
    plt.xlabel('#of Orders')

    renderStack.sort()
    x = []
    y = []
    q1 = statistics.median(renderStack[:math.floor((len(renderStack)/2))])
    q3 = statistics.median(renderStack[(math.floor(len(renderStack)/2)):])
    iqr = q3-q1
    top = q3+(1.5*iqr)

    for l in range(len(renderStack)):
        if(renderStack[l] <= top):

            y.append(renderStack[l])
            x.append(l)


    plt.step(x,y,color="#ff0000", label="Liquidity")
    plt.fill_between(x,y, color="#ff0000", step="pre", alpha=0.4)
    plt.legend()
    imf ="five_img"+str(random.randint(1,10000))+'.png'
    plt.savefig(imf)
    plt.clf()

    file = discord.File(imf)
    embedVar = discord.Embed(color=COLOR)
    embedVar.set_image(url="attachment://" + imf)

    await ctx.message.channel.send(embed=embedVar, file=file)
    os.remove(imf)


@bot.command()
async def osp(ctx):
    plist = []
    players = ctx.message.content.replace("f.osp ", "").upper()
    if ("," in players):
        # parse multiple players
        players = players.split(",")
        for i in range(len(players)):
            # remove extraneous white space
            temp_p = list(players[i])
            if (temp_p[0] == " "):
                temp_p = temp_p[1:]
            if (temp_p[-1] == " "):
                temp_p = temp_p[:-1]
            true_p = "".join(temp_p)
            plist.append(true_p)
    else:
        plist.append(players)
    if(len(plist) == 2 and plist[0] == plist[1]): #check doubles
        match_ids = []
        count = 0
        for i in range(len(datalink.player_by_id)):
            validate = False

            this_p = datalink.player_by_id[i]
            if(plist[0] == this_p[2] and plist[0] == this_p[3]):
                validate=True
            elif(plist[0] == this_p[4] and plist[0] == this_p[5]):
                validate=True

            if (validate):
                count += 1
                match_ids.append(str((datalink.player_by_id[i][0])))
    else:

        match_ids = []
        count = 0
        for i in range(len(datalink.player_by_id)):
            validate = True
            for j in plist:
                if (j not in datalink.player_by_id[i]):
                    validate = False
                    break
            if (validate):
                count += 1
                match_ids.append(str((datalink.player_by_id[i][0])))


    if (count == 0):
        pstr = " + ".join(plist)
        if(pstr == "F.OSP"):
            payload = "No players supplied."
        else:
            payload = "No matches for **" + pstr + "**"
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
        return None

    resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
    renderStack = []
    for j in range(len(resp["data"])):
        if(resp["data"][j]["token_id"] in match_ids):
            renderStack.append(resp["data"][j])

    if(renderStack == []):
        #none listed
        pstr = " + ".join(plist)
        payload = "No listings on OpenSea for **" + pstr + "**"
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
        return None

    pstr = " + ".join(plist)
    renderStack = sorted(renderStack, key=lambda d: d['eth_price'])
    payload = "\n**" + pstr + "** OpenSea Listings:\n" + "Floor: **" + str(renderStack[0]["eth_price"]) + " ETH | $" + str(
        round(renderStack[0]["eth_price"] * renderStack[0]["usd_eth_rate"], 2)) + "**"

    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))

    m = OSPages()
    await m.start(ctx, embed_var=embedVar, data=renderStack)



@bot.command()
async def floor(ctx):
    if(len(ctx.message.content.split(" ")) == 1):
        resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
        parsed_listings = {"0": [], "1": [], "2": [], "3": [], "4": []}
        rarity_breakdown_extra = datalink.rarity_breakdown_extra
        thisdic = {}
        for item in rarity_breakdown_extra:
            thisdic[str(item[0])] = item[-1]
        for j in range(len(resp["data"])):
            thisDicIndex = str(thisdic[str(resp["data"][j]["token_id"])])
            parsed_listings[thisDicIndex].append(resp["data"][j])


        # now sort them low to high
        for i in range(5):
            parsed_listings[str(i)] = sorted(parsed_listings[str(i)], key=lambda d: d['eth_price'])


        payload = "**General Floor Info:**"
        for i in range(5):
            if(parsed_listings[str(i)] != []):
                payload = payload + "\n" + str(i) + " Red Floor: **" + str(parsed_listings[str(i)][0]["eth_price"]) + " ETH | $" + str(round(parsed_listings[str(i)][0]["eth_price"]*parsed_listings[str(i)][0]["usd_eth_rate"],2)) + "**"
            if(parsed_listings[str(i)] == []):
                payload = payload + "\n" + str(i) + " Red Floor: **None Listed**"
        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(embed=embedVar)
    else:
        id = int(ctx.message.content.split(" ")[1])
        resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
        parsed_listings = {"0": [],"1": [],"2":[],"3":[],"4":[]}
        rarity_breakdown_extra = datalink.rarity_breakdown_extra
        thisdic = {}
        for item in rarity_breakdown_extra:
            thisdic[str(item[0])] = item[-1]
        for j in range(len(resp["data"])):
            thisDicIndex = str(thisdic[str(resp["data"][j]["token_id"])])
            parsed_listings[thisDicIndex].append(resp["data"][j])
        #now sort them low to high
        for i in range(4):
            parsed_listings[str(i)] = sorted( parsed_listings[str(i)], key=lambda d: d['eth_price'])

        thislist = parsed_listings[str(id)]

        if(thislist == []):
            embedVar = discord.Embed(title="", description="None listed.", color=COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(embed=embedVar)

        sweepreq = 0
        startp = thislist[0]["eth_price"]
        for j in range(len(thislist)):
            if(thislist[j]["eth_price"] == startp):
                sweepreq = sweepreq + startp
            else:
                break


        payload = "\n\n**" + str(id) +  " Red OpenSea Listings:**\n" + "Floor: **" + str(startp) + " ETH | $" + str(round(startp*thislist[0]["usd_eth_rate"],2)) +"**\n" + "Cost to Sweep: **" + str(sweepreq) + " ETH | $" + str(round(startp*thislist[0]["usd_eth_rate"],2)) +"**"

        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))

        m = OSPages()
        await m.start(ctx, embed_var=embedVar, data=thislist)

@bot.command()
async def gas(ctx):
    gasData = requests.get("https://ethgasapi.c4syner.repl.co/gas").json()["gas"]
    payload = "Low: **" + str(gasData["low"]) + "** Avg: **" + str(gasData["avg"]) + "** High: **" + str(gasData["high"]) + "**" + "\nMeasured in gwei"

    embedVar = discord.Embed(title="Ethereum Network Gas", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))
    await ctx.message.channel.send(embed=embedVar)

@bot.command()
async def info(ctx):
    payload = """
    **Stat Commands**
    `f.players` - Displays all available players and their respective positions. 
    `f.global_rarity` - Displays number of 4x rare, 3x rare, 2x rare, 1x rare, and commons that exist, as well the number of duplicate player Fives and their Token ID's. 
    `f.rarity <PLAYER>` - Displays drop rate and number of drops for queried player or group of comma separated players. Additionally, provides up to 10 matching ids.
    `f.id <TOKEN ID>` - Displays a *Fives* team's rarity, based on each individual player's drop rates. As well as the team's rarity rank out of all tokens. 
    `f.img <TOKEN ID>` - Displays a *Fives* team.
    `f.floor <Optional #OF RARES>` - If number of rares is supplied, bot will provide all OpenSea listings that match it. If no arguments are supplied, bot will provide current floors for every number of rares.
    `f.orderbook <PLAYER>` - Scrapes the entire orderbook on OpenSea of all open sell orders and plots all of them within 1.5xIQR of the dataset of tokens that contain your specified player or players.
    `f.osp <PLAYER>` - Provides all OpenSea listings that match a supplied player or collection of players.
    `f.rank_list` - Provides every fives team iterable by its calculated team rank.
    `f.florderbook <# OF RARES>` - Scrapes the entire orderbook on OpenSea of all open sell orders and plots all of them within 1.5xIQR of the dataset of tokens that contain your specified number of rares.
    **Gas Commands**
    `f.gas` - Provides the current ethereum network gas fee. 
    `f.gasph` - Provides the past hour of gas price action (Update once per minute).
    `f.gas_ping <GWEI (30,40,50,60)>` - Will ping you when gas drops below your specifed gwei, there is a 30 minute timeout whenever a gas ping is sent.
    `f.purge_pings` - Will remove all gas related roles.
    """

    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))
    await ctx.message.channel.send(embed=embedVar)

@bot.command()
async def rank_list(ctx):
    tlist = []
    i = 0
    for item in datalink.sorted_rankings:
        i += 1
        tlist.append("#" + (str(i) + " " + str(item[0])))
    payload = "\n\n**Fives Ranked:**"
    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project Fives"))

    m = RarityPages()
    await m.start(ctx, embed_var=embedVar, data=tlist)

time30 = ["30 Gas Alerts", 1800]
time40 = ["40 Gas Alerts", 1800]
time50 = ["50 Gas Alerts", 1800]
time60 = ["60 Gas Alerts", 1800]

@bot.command()
async def gas_ping(ctx):
    print("executed")
    global time30,time40,time50,time60
    member = ctx.message.author
    id = (ctx.message.content.split(" ")[1])
    server_id = 885017275449634876
    this_guild = bot.get_guild(server_id)
    role30 = get(this_guild.roles, name=time30[0])
    role40 = get(this_guild.roles, name=time40[0])
    role50 = get(this_guild.roles, name=time50[0])
    role60 = get(this_guild.roles, name=time60[0])

    if(id == "30"):
        await member.add_roles(role30)
        await ctx.message.channel.send("Success adding `" + id + " Gas Alerts` to " + member.mention)
    elif (id == "40"):
        await member.add_roles(role40)
        await ctx.message.channel.send("Success adding `" + id + " Gas Alerts` to " + member.mention)
    elif (id == "50"):
        await member.add_roles(role50)
        await ctx.message.channel.send("Success adding `" + id + " Gas Alerts` to " + member.mention)
    elif (id == "60"):
        await member.add_roles(role60)
        await ctx.message.channel.send("Success adding `" + id + " Gas Alerts` to " + member.mention)
    else:
        await ctx.message.channel.send("Invalid Value: Try `30,40,50,60`")


@bot.command()
async def purge_pings(ctx):
    print("executed")
    global time30, time40, time50, time60
    member = ctx.message.author
    server_id = 885017275449634876
    this_guild = bot.get_guild(server_id)
    role30 = get(this_guild.roles, name=time30[0])
    role40 = get(this_guild.roles, name=time40[0])
    role50 = get(this_guild.roles, name=time50[0])
    role60 = get(this_guild.roles, name=time60[0])

    await member.remove_roles(role30)
    await member.remove_roles(role40)
    await member.remove_roles(role50)
    await member.remove_roles(role60)

    await ctx.message.channel.send("Removed all Gas Roles from " + member.mention)


@bot.command()
async def id(ctx):
    id = int(ctx.message.content.split(" ")[1])

    this_player = None
    for i in datalink.player_by_id:
        if(i[0] == id):
            this_player = i
            break

    if(this_player == None):
        #not real id
        payload = "**" + str(id) + "** is not a valid Fives team."

        embedVar = discord.Embed(title="", description=payload, color=COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(embed=embedVar)
        return None

    player_data = []

    # we gucci tldr
    for i in range(len(this_player)):
        if(i != 0):
            plist = [this_player[i]]
            count = 0
            for f in range(len(datalink.player_by_id)):
                validate = True
                for j in plist:
                    if (j not in datalink.player_by_id[f]):
                        validate = False
                        break
                if (validate):
                    count += 1
            rarity = 0
            if(this_player[i] in datalink.legendaryWings or this_player[i] in datalink.legendaryBackcourt or this_player[i] in datalink.legendaryBigMen):
                rarity = 1
            player_data.append([this_player[i],count, rarity])
    avg_drop = 0
    for dropnum in player_data:
        avg_drop = avg_drop + dropnum[1]
    avg_drop = round(avg_drop/5, 3)
    avg_rarity = round((avg_drop/8000)*100, 5)


    player_data = player_data
    this_player = this_player
    id = id
    title = "**#" + str(id) + "**\n"
    players = ""
    for player in player_data:
        if(player[2] == 1):
            players = players + "```diff\n- " + player[0] + "```"
        else:
            players = players + "```\n- " + player[0] + "```"


    #get rank
    j = 0
    for h in datalink.sorted_rankings:
        j+=1
        if(h[0] == id):
            break

    foot = "\n**Rarity and Rank:**\nAvg Player Drop Count: **" + str(avg_drop) + "**\nRank: **" + str(j) + "**"
    payload = title + players + foot

    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))
    await ctx.message.channel.send(embed=embedVar)

@bot.command()
async def global_rarity(ctx):
    fours = 0
    threes = 0
    twos = 0
    ones = 0
    zeros = 0
    for i in range(len(datalink.rarity_ranked)):
        dp = datalink.rarity_ranked[(len(datalink.rarity_ranked)-1)-i]
        if(dp[1] == 4):
            fours += 1
        if(dp[1] == 3):
            threes += 1
        if(dp[1] == 2):
            twos += 1
        if(dp[1] == 1):
            ones += 1
        if(dp[1] == 0):
            zeros += 1

    fp = str(round(100*(fours/8000), 5))
    tp = str(round(100*(threes/8000), 5))
    twp = str(round(100 * (twos / 8000), 5))
    op = str(round(100 * (ones / 8000), 5))
    zs = str(round(100 * (zeros / 8000), 5))

    double_rares = 0
    formatted_dupes = "```"
    player_list = datalink.player_by_id
    for i in range(len(player_list)):
        if (player_list[i][2] == player_list[i][3]):
            formatted_dupes = formatted_dupes + "\n" + str(player_list[i][0])
            double_rares += 1
        if (player_list[i][4] == player_list[i][5]):
            formatted_dupes = formatted_dupes + "\n"+ str(player_list[i][0])

            double_rares += 1
    formatted_dupes = formatted_dupes + "```"
    dr = str(round(100 * (double_rares / 8000), 5))


    payload = "**RARITY DROP COUNTS**\nTotal *Fives*: **8000**\nTotal Rare *Fives*: **3210**\nPercentage Rare *Fives*: **40.125%**\n\n**4x Rares:**\n" + "# of Drops: **" + str(fours) + "**\nDrop Rate: **" + fp + "%**\n**3x Rares:**\n" + "# of Drops: **" + str(threes) + "**\nDrop Rate: **" + tp + "%**\n**2x Rares:**\n" + "# of Drops: **" + str(twos) + "**\nDrop Rate: **" + twp + "%**\n**1x Rares:**\n" + "# of Drops: **" + str(ones) + "**\nDrop Rate: **" + op + "%**\n**Commons:**\n" + "# of Drops: **" + str(zeros) + "**\nDrop Rate: **" + zs + "%**"
    payload = payload + "\n\n**Duplicate Players:**\n" + "# of Drops: **" + str(double_rares) + "**\nDrop Rate: **" + dr + "%**" + "\nToken ID's: " + formatted_dupes
    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))
    await ctx.message.channel.send(embed=embedVar)

@bot.command()
async def players(ctx):
    pg_text = "**Point Guards**```"
    for i in datalink.pointGuards:
        this_text = "\n" + str(i)
        pg_text = pg_text + this_text
    pg_text = pg_text + "```"

    sg_text = "**Shooting Guards**```"
    for i in datalink.shootingGuards:
        this_text = "\n" + str(i)
        sg_text = sg_text + this_text
    sg_text = sg_text + "```"

    sf_text = "**Small Forwards**```"
    for i in datalink.smallForwards:
        this_text = "\n" + str(i)
        sf_text = sf_text + this_text
    sf_text = sf_text + "```"

    pf_text = "**Power Forwards**```"
    for i in datalink.powerForwards:
        this_text = "\n" + str(i)
        pf_text = pf_text + this_text
    pf_text = pf_text + "```"

    c_text = "**Centers**```"
    for i in datalink.centers:
        this_text = "\n" + str(i)
        c_text = c_text + this_text
    c_text = c_text + "```"

    lb_text = "**Legendary Backcourt**```"
    for i in datalink.legendaryBackcourt:
        this_text = "\n" + str(i)
        lb_text = lb_text + this_text
    lb_text = lb_text + "```"

    lw_text = "**Legendary Wings**```"
    for i in datalink.legendaryWings:
        this_text = "\n" + str(i)
        lw_text = lw_text + this_text
    lw_text = lw_text + "```"

    lbig_text = "**Legendary Bigmen**```"
    for i in datalink.legendaryBigMen:
        this_text = "\n" + str(i)
        lbig_text = lbig_text + this_text
    lbig_text = lbig_text + "```"

    payload = "**COMMONS:**\n\n" + pg_text + "\n" + sg_text + "\n" + sf_text + "\n" + pf_text + "\n" + c_text + "\n\n**LEGENDS:**\n\n" + lb_text + "\n" + lw_text + "\n" + lbig_text


    embedVar = discord.Embed(title="", description=payload, color=COLOR)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project Fives"))
    await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)


@bot.command()
async def img(ctx):
    id = int(ctx.message.content.split(" ")[1])

    this_url = oss.single_asset(id)["image_url"]

    svg_source = requests.get(this_url).text


    with open("source.svg", "w") as file:
        file.write(svg_source)

    drawing = svg2rlg("source.svg")
    renderPM.drawToFile(drawing, "t_img.png", fmt="PNG")

    file = discord.File("t_img.png")

    payload = ""
    embedVar = discord.Embed(title="Fives #" + str(id) ,description=payload, color=0xFF0000)
    embedVar.timestamp = datetime.utcnow()
    embedVar.set_footer(text=("Project FIVES"))
    embedVar.set_image(url="attachment://t_img.png")
    await ctx.message.channel.send(embed=embedVar, file=file)

@tasks.loop(seconds = 10) # repeat after every 10 seconds
async def pingGas():
    await bot.wait_until_ready()
    global time30,time40,time50,time60
    channel_id = 893010436948111361
    server_id = 885017275449634876
    this_guild = bot.get_guild(server_id)
    role30 = get(this_guild.roles, name=time30[0])
    role40 = get(this_guild.roles, name=time40[0])
    role50 = get(this_guild.roles, name=time50[0])
    role60 = get(this_guild.roles, name=time60[0])
    this_channel = bot.get_channel(channel_id)

    gasAvg = requests.get("https://ethgasapi.c4syner.repl.co/gas").json()["gas"]["avg"]
    if(gasAvg <= 60 and time.time()-time60[1] >= 1800):
        await this_channel.send(role60.mention)
        time60[1] = time.time()

    if (gasAvg <= 50 and time.time() - time50[1] >= 1800):
        await this_channel.send(role50.mention)
        time50[1] = time.time()

    if (gasAvg <= 40 and time.time() - time40[1] >= 1800):
        await this_channel.send(role40.mention)
        time40[1] = time.time()

    if (gasAvg <= 30 and time.time() - time30[1] >= 1800):
        await this_channel.send(role30.mention)
        time30[1] = time.time()




pingGas.start()

bot.run("ODg2ODcxNzIzMzk0MzYzNDAz.YT75qA.wtfxl-4zr78epBRShRW7STb3P18")