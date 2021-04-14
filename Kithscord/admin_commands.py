import discord

from overload import *
import util


@export(-1)
async def cool(args, msg: discord.Message, response: discord.Message):
    await util.edit_embed(response, "bruh", "bruh")
