import discord

from overload import *
import util


@export(-1, True)
async def error(args, msg: discord.Message, response: discord.Message):
    raise Exception("bruh", "bruh")
