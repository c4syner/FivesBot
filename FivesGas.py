from discord.ext import commands
import requests

bot = commands.Bot(command_prefix=['!', '.'], help_command=None)
COLOR=0xff0000

#Eth gas price
@bot.command()
async def gas(ctx):
    eth_gas = requests.get("https://ethgasapi.c4syner.repl.co/gas").json
    print(eth_gas)

bot.run("")
