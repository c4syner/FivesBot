import discord
from discord.ext import menus
from typing import List
import copy
import math

class RarityPages(menus.Menu):
    def __init__(self, embed_var: discord.Embed, data: List):
        super(RarityPages, self).__init__()
        self.embed_var = embed_var
        self.iter_var = 0
        self.data = data
        self.iter_cap = 10

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
    def __init__(self, embed_var: discord.Embed, data: List):
        super(OSPages, self).__init__()
        self.embed_var = embed_var
        self.iter_var = 0
        self.data = data
        self.iter_cap = 10

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

