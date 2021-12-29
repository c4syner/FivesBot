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
from typing import List
from util import fives_data, opensea, menu_sets

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import requests

import matplotlib.pyplot as plt
import os


class FivesFunctions():
    def __init__(self, CONTRACT: str, OS_API: str, COLOR: int):
        self.oss = opensea.OpenSea(ETH_CONTRACT=CONTRACT, API_KEY=OS_API)
        self.CONTRACT = CONTRACT
        self.datalink = fives_data.FivesData()
        self.COLOR = COLOR

    async def fives_rarity(self, ctx):
        """
        Provides a mutable discord embed with token ids that match a given player/s.
        :param ctx: Discord Command Parameter
        :return: Mutable Discord Menu Object
        """
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
        if (len(plist) == 2 and plist[0] == plist[1]):  # check doubles
            match_ids = []
            count = 0
            for i in range(len(self.datalink.player_by_id)):
                validate = False

                this_p = self.datalink.player_by_id[i]
                if (plist[0] == this_p[2] and plist[0] == this_p[3]):
                    validate = True
                elif (plist[0] == this_p[4] and plist[0] == this_p[5]):
                    validate = True

                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))
        else:

            match_ids = []
            count = 0
            for i in range(len(self.datalink.player_by_id)):
                validate = True
                for j in plist:
                    if (j not in self.datalink.player_by_id[i]):
                        validate = False
                        break
                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))

        if (count == 0):
            pstr = " + ".join(plist)
            payload = "No matches for **" + pstr + "**"
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
            return None

        percent = round((count / 8000) * 100, 4)
        pstr = " + ".join(plist)
        payload = "**" + pstr + ":**\n" + "# of Drops: **" + str(count) + "**\nDrop Rate: **" + str(percent) + "%**"
        payload = payload + "\n\n**Matching Teams:**"
        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project Fives"))

        m = menu_sets.RarityPages(embedVar,match_ids)
        await m.start(ctx)

    async def fives_orderbook(self, ctx):
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
            for i in range(len(self.datalink.player_by_id)):
                validate = False

                this_p = self.datalink.player_by_id[i]
                if (plist[0] == this_p[2] and plist[0] == this_p[3]):
                    validate = True
                elif (plist[0] == this_p[4] and plist[0] == this_p[5]):
                    validate = True

                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))
        else:

            match_ids = []
            count = 0
            for i in range(len(self.datalink.player_by_id)):
                validate = True
                for j in plist:
                    if (j not in self.datalink.player_by_id[i]):
                        validate = False
                        break
                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))

        if (count == 0):
            pstr = " + ".join(plist)
            if (pstr == "F.ORDERBOOK"):
                payload = "No players supplied."
            else:
                payload = "No matches for **" + pstr + "**"
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
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
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
            return None
        pstr = " + ".join(plist)

        # Create orderbook image

        plt.style.use('dark_background')
        plt.title(pstr + " Orderbook")
        plt.ylabel('Ether')
        plt.xlabel('#of Orders')

        renderStack.sort()
        x = []
        y = []
        q1 = statistics.median(renderStack[:math.floor((len(renderStack) / 2))])
        q3 = statistics.median(renderStack[(math.floor(len(renderStack) / 2)):])
        iqr = q3 - q1
        top = q3 + (1.5 * iqr)

        for l in range(len(renderStack)):
            if (renderStack[l] <= top):
                y.append(renderStack[l])
                x.append(l)

        plt.step(x, y, color="#ff0000", label="Liquidity")
        plt.fill_between(x, y, color="#ff0000", step="pre", alpha=0.4)
        plt.legend()
        imf = "five_img" + str(random.randint(1, 10000)) + '.png'
        plt.savefig(imf)
        plt.clf()

        file = discord.File(imf)
        embedVar = discord.Embed(color=self.COLOR)
        embedVar.set_image(url="attachment://" + imf)

        await ctx.message.channel.send(embed=embedVar, file=file)
        os.remove(imf)

    async def fives_floor_orderbook(self, ctx):
        id = int(ctx.message.content.split(" ")[1])
        match_ids = []
        for i in range(len(self.datalink.rarity_breakdown_extra)):
            if (self.datalink.rarity_breakdown_extra[i][-1] == id):
                match_ids.append(self.datalink.rarity_breakdown_extra[i][0])

        resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
        renderStack = []
        for j in range(len(resp["data"])):
            if (int(resp["data"][j]["token_id"]) in match_ids):
                renderStack.append(resp["data"][j]["eth_price"])

        if (renderStack == []):
            # none listed
            payload = "No listings on OpenSea."
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
            return None

        # Create orderbook image

        plt.style.use('dark_background')
        plt.title(str(id) + " Red" + " Orderbook")
        plt.ylabel('Ether')
        plt.xlabel('#of Orders')

        renderStack.sort()
        x = []
        y = []
        q1 = statistics.median(renderStack[:math.floor((len(renderStack) / 2))])
        q3 = statistics.median(renderStack[(math.floor(len(renderStack) / 2)):])
        iqr = q3 - q1
        top = q3 + (1.5 * iqr)

        for l in range(len(renderStack)):
            if (renderStack[l] <= top):
                y.append(renderStack[l])
                x.append(l)

        plt.step(x, y, color="#ff0000", label="Liquidity")
        plt.fill_between(x, y, color="#ff0000", step="pre", alpha=0.4)
        plt.legend()
        imf = "five_img" + str(random.randint(1, 10000)) + '.png'
        plt.savefig(imf)
        plt.clf()

        file = discord.File(imf)
        embedVar = discord.Embed(color=self.COLOR)
        embedVar.set_image(url="attachment://" + imf)

        await ctx.message.channel.send(embed=embedVar, file=file)
        os.remove(imf)

    async def fives_players(self, ctx):
        pg_text = "**Point Guards**```"
        for i in self.datalink.pointGuards:
            this_text = "\n" + str(i)
            pg_text = pg_text + this_text
        pg_text = pg_text + "```"

        sg_text = "**Shooting Guards**```"
        for i in self.datalink.shootingGuards:
            this_text = "\n" + str(i)
            sg_text = sg_text + this_text
        sg_text = sg_text + "```"

        sf_text = "**Small Forwards**```"
        for i in self.datalink.smallForwards:
            this_text = "\n" + str(i)
            sf_text = sf_text + this_text
        sf_text = sf_text + "```"

        pf_text = "**Power Forwards**```"
        for i in self.datalink.powerForwards:
            this_text = "\n" + str(i)
            pf_text = pf_text + this_text
        pf_text = pf_text + "```"

        c_text = "**Centers**```"
        for i in self.datalink.centers:
            this_text = "\n" + str(i)
            c_text = c_text + this_text
        c_text = c_text + "```"

        lb_text = "**Legendary Backcourt**```"
        for i in self.datalink.legendaryBackcourt:
            this_text = "\n" + str(i)
            lb_text = lb_text + this_text
        lb_text = lb_text + "```"

        lw_text = "**Legendary Wings**```"
        for i in self.datalink.legendaryWings:
            this_text = "\n" + str(i)
            lw_text = lw_text + this_text
        lw_text = lw_text + "```"

        lbig_text = "**Legendary Bigmen**```"
        for i in self.datalink.legendaryBigMen:
            this_text = "\n" + str(i)
            lbig_text = lbig_text + this_text
        lbig_text = lbig_text + "```"

        payload = "**COMMONS:**\n\n" + pg_text + "\n" + sg_text + "\n" + sf_text + "\n" + pf_text + "\n" + c_text + "\n\n**LEGENDS:**\n\n" + lb_text + "\n" + lw_text + "\n" + lbig_text

        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project Fives"))
        await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)

    async def fives_drops(self, ctx):
        fours = 0
        threes = 0
        twos = 0
        ones = 0
        zeros = 0
        for i in range(len(self.datalink.rarity_ranked)):
            dp = self.datalink.rarity_ranked[(len(self.datalink.rarity_ranked) - 1) - i]
            if (dp[1] == 4):
                fours += 1
            if (dp[1] == 3):
                threes += 1
            if (dp[1] == 2):
                twos += 1
            if (dp[1] == 1):
                ones += 1
            if (dp[1] == 0):
                zeros += 1

        fp = str(round(100 * (fours / 8000), 5))
        tp = str(round(100 * (threes / 8000), 5))
        twp = str(round(100 * (twos / 8000), 5))
        op = str(round(100 * (ones / 8000), 5))
        zs = str(round(100 * (zeros / 8000), 5))

        double_rares = 0
        formatted_dupes = "```"
        player_list = self.datalink.player_by_id
        for i in range(len(player_list)):
            if (player_list[i][2] == player_list[i][3]):
                formatted_dupes = formatted_dupes + "\n" + str(player_list[i][0])
                double_rares += 1
            if (player_list[i][4] == player_list[i][5]):
                formatted_dupes = formatted_dupes + "\n" + str(player_list[i][0])

                double_rares += 1
        formatted_dupes = formatted_dupes + "```"
        dr = str(round(100 * (double_rares / 8000), 5))

        payload = "**RARITY DROP COUNTS**\nTotal *Fives*: **8000**\nTotal Rare *Fives*: **3210**\nPercentage Rare *Fives*: **40.125%**\n\n**4x Rares:**\n" + "# of Drops: **" + str(
            fours) + "**\nDrop Rate: **" + fp + "%**\n**3x Rares:**\n" + "# of Drops: **" + str(
            threes) + "**\nDrop Rate: **" + tp + "%**\n**2x Rares:**\n" + "# of Drops: **" + str(
            twos) + "**\nDrop Rate: **" + twp + "%**\n**1x Rares:**\n" + "# of Drops: **" + str(
            ones) + "**\nDrop Rate: **" + op + "%**\n**Commons:**\n" + "# of Drops: **" + str(
            zeros) + "**\nDrop Rate: **" + zs + "%**"
        payload = payload + "\n\n**Duplicate Players:**\n" + "# of Drops: **" + str(
            double_rares) + "**\nDrop Rate: **" + dr + "%**" + "\nToken ID's: " + formatted_dupes
        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(embed=embedVar)

    async def fives_rank(self, ctx):
        id = int(ctx.message.content.split(" ")[1])
        this_player = None
        for i in self.datalink.player_by_id:
            if (i[0] == id):
                this_player = i
                break

        if (this_player == None):
            # not real id
            payload = "**" + str(id) + "** is not a valid Fives team."

            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(embed=embedVar)
            return None

        player_data = []

        # we gucci tldr
        for i in range(len(this_player)):
            if (i != 0):
                plist = [this_player[i]]
                count = 0
                for f in range(len(self.datalink.player_by_id)):
                    validate = True
                    for j in plist:
                        if (j not in self.datalink.player_by_id[f]):
                            validate = False
                            break
                    if (validate):
                        count += 1
                rarity = 0
                if (this_player[i] in self.datalink.legendaryWings or this_player[i] in self.datalink.legendaryBackcourt or
                        this_player[i] in self.datalink.legendaryBigMen):
                    rarity = 1
                player_data.append([this_player[i], count, rarity])
        avg_drop = 0
        for dropnum in player_data:
            avg_drop = avg_drop + dropnum[1]
        avg_drop = round(avg_drop / 5, 3)
        avg_rarity = round((avg_drop / 8000) * 100, 5)

        player_data = player_data
        this_player = this_player
        id = id
        title = "**#" + str(id) + "**\n"
        players = ""
        for player in player_data:
            if (player[2] == 1):
                players = players + "```diff\n- " + player[0] + "```"
            else:
                players = players + "```\n- " + player[0] + "```"

        # get rank
        j = 0
        for h in self.datalink.sorted_rankings:
            j += 1
            if (h[0] == id):
                break

        foot = "\n**Rarity and Rank:**\nAvg Player Drop Count: **" + str(avg_drop) + "**\nRank: **" + str(j) + "**"
        payload = title + players + foot

        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(embed=embedVar)

    async def fives_rare_floor(self, ctx):
        if (len(ctx.message.content.split(" ")) == 1):
            resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
            parsed_listings = {"0": [], "1": [], "2": [], "3": [], "4": []}
            rarity_breakdown_extra = self.datalink.rarity_breakdown_extra
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
                if (parsed_listings[str(i)] != []):
                    payload = payload + "\n" + str(i) + " Red Floor: **" + str(
                        parsed_listings[str(i)][0]["eth_price"]) + " ETH | $" + str(
                        round(parsed_listings[str(i)][0]["eth_price"] * parsed_listings[str(i)][0]["usd_eth_rate"],
                              2)) + "**"
                if (parsed_listings[str(i)] == []):
                    payload = payload + "\n" + str(i) + " Red Floor: **None Listed**"
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(embed=embedVar)
        else:
            id = int(ctx.message.content.split(" ")[1])
            resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
            parsed_listings = {"0": [], "1": [], "2": [], "3": [], "4": []}
            rarity_breakdown_extra = self.datalink.rarity_breakdown_extra
            thisdic = {}
            for item in rarity_breakdown_extra:
                thisdic[str(item[0])] = item[-1]
            for j in range(len(resp["data"])):
                thisDicIndex = str(thisdic[str(resp["data"][j]["token_id"])])
                parsed_listings[thisDicIndex].append(resp["data"][j])
            # now sort them low to high
            for i in range(4):
                parsed_listings[str(i)] = sorted(parsed_listings[str(i)], key=lambda d: d['eth_price'])

            thislist = parsed_listings[str(id)]

            if (thislist == []):
                embedVar = discord.Embed(title="", description="None listed.", color=self.COLOR)
                embedVar.timestamp = datetime.utcnow()
                embedVar.set_footer(text=("Project FIVES"))
                await ctx.message.channel.send(embed=embedVar)

            sweepreq = 0
            startp = thislist[0]["eth_price"]
            for j in range(len(thislist)):
                if (thislist[j]["eth_price"] == startp):
                    sweepreq = sweepreq + startp
                else:
                    break

            payload = "\n\n**" + str(id) + " Red OpenSea Listings:**\n" + "Floor: **" + str(startp) + " ETH | $" + str(
                round(startp * thislist[0]["usd_eth_rate"], 2)) + "**\n" + "Cost to Sweep: **" + str(
                sweepreq) + " ETH | $" + str(round(startp * thislist[0]["usd_eth_rate"], 2)) + "**"

            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))

            m = menu_sets.OSPages(embed_var=embedVar, data=thislist)
            await m.start(ctx)

    async def fives_orderbook(self, ctx):
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
            for i in range(len(self.datalink.player_by_id)):
                validate = False

                this_p = self.datalink.player_by_id[i]
                if (plist[0] == this_p[2] and plist[0] == this_p[3]):
                    validate = True
                elif (plist[0] == this_p[4] and plist[0] == this_p[5]):
                    validate = True

                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))
        else:

            match_ids = []
            count = 0
            for i in range(len(self.datalink.player_by_id)):
                validate = True
                for j in plist:
                    if (j not in self.datalink.player_by_id[i]):
                        validate = False
                        break
                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))

        if (count == 0):
            pstr = " + ".join(plist)
            if (pstr == "F.ORDERBOOK"):
                payload = "No players supplied."
            else:
                payload = "No matches for **" + pstr + "**"
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
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
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
            return None
        pstr = " + ".join(plist)

        # Create orderbook image

        plt.style.use('dark_background')
        plt.title(pstr + " Orderbook")
        plt.ylabel('Ether')
        plt.xlabel('#of Orders')

        renderStack.sort()
        x = []
        y = []
        q1 = statistics.median(renderStack[:math.floor((len(renderStack) / 2))])
        q3 = statistics.median(renderStack[(math.floor(len(renderStack) / 2)):])
        iqr = q3 - q1
        top = q3 + (1.5 * iqr)

        for l in range(len(renderStack)):
            if (renderStack[l] <= top):
                y.append(renderStack[l])
                x.append(l)

        plt.step(x, y, color="#ff0000", label="Liquidity")
        plt.fill_between(x, y, color="#ff0000", step="pre", alpha=0.4)
        plt.legend()
        imf = "five_img" + str(random.randint(1, 10000)) + '.png'
        plt.savefig(imf)
        plt.clf()

        file = discord.File(imf)
        embedVar = discord.Embed(color=self.COLOR)
        embedVar.set_image(url="attachment://" + imf)

        await ctx.message.channel.send(embed=embedVar, file=file)
        os.remove(imf)

    async def fives_osp(self, ctx):
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
        if (len(plist) == 2 and plist[0] == plist[1]):  # check doubles
            match_ids = []
            count = 0
            for i in range(len(self.datalink.player_by_id)):
                validate = False

                this_p = self.datalink.player_by_id[i]
                if (plist[0] == this_p[2] and plist[0] == this_p[3]):
                    validate = True
                elif (plist[0] == this_p[4] and plist[0] == this_p[5]):
                    validate = True

                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))
        else:

            match_ids = []
            count = 0
            for i in range(len(self.datalink.player_by_id)):
                validate = True
                for j in plist:
                    if (j not in self.datalink.player_by_id[i]):
                        validate = False
                        break
                if (validate):
                    count += 1
                    match_ids.append(str((self.datalink.player_by_id[i][0])))

        if (count == 0):
            pstr = " + ".join(plist)
            if (pstr == "F.OSP"):
                payload = "No players supplied."
            else:
                payload = "No matches for **" + pstr + "**"
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
            return None

        resp = requests.get("https://osfiveslisting.c4syner.repl.co/fives_os.json").json()
        renderStack = []
        for j in range(len(resp["data"])):
            if (resp["data"][j]["token_id"] in match_ids):
                renderStack.append(resp["data"][j])

        if (renderStack == []):
            # none listed
            pstr = " + ".join(plist)
            payload = "No listings on OpenSea for **" + pstr + "**"
            embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
            embedVar.timestamp = datetime.utcnow()
            embedVar.set_footer(text=("Project FIVES"))
            await ctx.message.channel.send(ctx.message.author.mention, embed=embedVar)
            return None

        pstr = " + ".join(plist)
        renderStack = sorted(renderStack, key=lambda d: d['eth_price'])
        payload = "\n**" + pstr + "** OpenSea Listings:\n" + "Floor: **" + str(
            renderStack[0]["eth_price"]) + " ETH | $" + str(
            round(renderStack[0]["eth_price"] * renderStack[0]["usd_eth_rate"], 2)) + "**"

        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))

        m = menu_sets.OSPages(embed_var=embedVar, data=renderStack)
        await m.start(ctx)


    async def fives_image(self, ctx):
        id = int(ctx.message.content.split(" ")[1])

        this_url = self.oss.single_asset(id)["image_url"]

        svg_source = requests.get(this_url).text

        with open("stat.svg", "w") as file:
            file.write(svg_source)

        drawing = svg2rlg("stat.svg")
        renderPM.drawToFile(drawing, "stat.png", fmt="PNG")

        file = discord.File("stat.png")

        payload = ""
        embedVar = discord.Embed(title="Fives #" + str(id) ,description=payload, color=0xFF0000)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        embedVar.set_image(url="attachment://stat.png")
        await ctx.message.channel.send(embed=embedVar, file=file)

    async def fives_info(self, ctx):
        payload = """
        **Commands**
        `f.players` - Displays all available players and their respective positions. 
        
        `f.drops` - Displays number of 4x rare, 3x rare, 2x rare, 1x rare, and commons that exist, as well the number of duplicate player Fives and their Token ID's. 
        
        `f.rarity <PLAYER>` - Displays drop rate and number of drops for queried player or group of comma separated players. Additionally, provides up to 10 matching ids.
        
        `f.rank <TOKEN ID>` - Displays a *Fives* team's rarity, based on each individual player's drop rates. As well as the team's rarity rank out of all tokens. 
        
        `f.img <TOKEN ID>` - Displays a *Fives* team.
        
        `f.floor <Optional #OF RARES>` - If number of rares is supplied, bot will provide all OpenSea listings that match it. If no arguments are supplied, bot will provide current floors for every number of rares.
        
        `f.orderbook <PLAYER>` - Scrapes the entire orderbook on OpenSea of all open sell orders and plots all of them within 1.5xIQR of the dataset of tokens that contain your specified player or players.
        
        `f.osp <PLAYER>` - Provides all OpenSea listings that match a supplied player or collection of players.
        
        `f.rank_list` - Provides every fives team iterable by its calculated team rank.
        
        `f.floor_orderbook <# OF RARES>` - Scrapes the entire orderbook on OpenSea of all open sell orders and plots all of them within 1.5xIQR of the dataset of tokens that contain your specified number of rares.
        """

        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project FIVES"))
        await ctx.message.channel.send(embed=embedVar)
    
    async def fives_rank_list(self, ctx):
        tlist = []
        i = 0
        for item in self.datalink.sorted_rankings:
            i += 1
            tlist.append("#" + (str(i) + " " + str(item[0])))
        payload = "\n\n**Fives Ranked:**"
        embedVar = discord.Embed(title="", description=payload, color=self.COLOR)
        embedVar.timestamp = datetime.utcnow()
        embedVar.set_footer(text=("Project Fives"))

        m = menu_sets.RarityPages(embed_var=embedVar, data=tlist)
        await m.start(ctx)