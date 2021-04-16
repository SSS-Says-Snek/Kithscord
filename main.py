import os

import discord

from kithscord import admin_commands, common, user_commands, util


@common.bot.event
async def on_ready():
    """
    The initial start when Kithscord gets booted.
    """
    util.log("Kithscord ready!")


@common.bot.event
async def on_message(msg: discord.Message):
    """
    When a message is sent.
    """
    if msg.author.bot:
        return

    if msg.content.startswith(common.PREFIX):
        cmd = user_commands.UserCommand()
        for role in msg.author.roles:
            if role.id in common.ADMIN_ROLES:
                cmd = admin_commands.AdminCommand()
                break

        response = await util.send_embed(
            msg.channel, "", "Your command is being processed!"
        )
        await cmd.handle_cmd(msg, response)

common.bot.run(os.environ["TOKEN"])
