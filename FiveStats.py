from fives_bot_functions import FivesFunctions
from discord.ext import commands

fives_obj = FivesFunctions(
    CONTRACT="0x017Ba9AC7916ebd646e7c11DD220c05c5b790224",
    OS_API="2d5ca92fcfe849389a0cf12b73df9340",
    COLOR=0xff0000
)

bot = commands.Bot(command_prefix=['f.','F.'], help_command=None)

#Stat Commands
@bot.command()
async def rarity(ctx):
    await fives_obj.fives_rarity(ctx)

@bot.command()
async def floor_orderbook(ctx):
    await fives_obj.fives_floor_orderbook(ctx)

@bot.command()
async def players(ctx):
    await fives_obj.fives_players(ctx)

@bot.command()
async def drops(ctx):
    await fives_obj.fives_drops(ctx)

@bot.command()
async def rank(ctx):
    await fives_obj.fives_rank(ctx)

@bot.command()
async def floor(ctx):
    await fives_obj.fives_rare_floor(ctx)

@bot.command()
async def orderbook(ctx):
    await fives_obj.fives_orderbook(ctx)

@bot.command()
async def osp(ctx):
    await fives_obj.fives_osp(ctx)

@bot.command()
async def img(ctx):
    await fives_obj.fives_image(ctx)

@bot.command()
async def rank_list(ctx):
    await fives_obj.fives_rank_list(ctx)

@bot.command()
async def info(ctx):
    await fives_obj.fives_info(ctx)

@bot.command()
async def help(ctx):
    await fives_obj.fives_info(ctx)

bot.run("ODg2ODcxNzIzMzk0MzYzNDAz.YT75qA.J1B4h1qYZeCz4nUF0taKsIQAD1Y")