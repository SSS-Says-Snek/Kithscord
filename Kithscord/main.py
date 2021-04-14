import discord
import os

import commands
import common
import util


@common.bot.event
async def on_ready():
    """
    The initial start when Kithscord gets booted.
    """
    await util.log("Kithscord ready!")


@common.bot.event
async def on_message(msg: discord.Message):
    """
    When a message is sent.
    """
    if msg.author.bot:
        return

    if msg.content.startswith(os.environ["PREFIX"]):
        response = await util.send_embed(msg.channel, "", "Your command is being processed!")
        await commands.handle(msg.content[len(os.environ["PREFIX"]):].lstrip().rstrip(), msg, response)

common.bot.run(os.environ["TOKEN"])
