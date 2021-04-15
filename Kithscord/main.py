import discord
import os

import common
import util
import user_commands
import admin_commands

admin = admin_commands.AdminCommand()
user = user_commands.UserCommand()


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

    if msg.content.startswith(common.PREFIX):
        cmd = user
        for role in msg.author.roles:
            if role.id in common.ADMIN_ROLES:
                cmd = admin
                break

        response = await util.send_embed(
            msg.channel, "", "Your command is being processed!"
        )
        await cmd.handle_cmd(msg, response)

common.bot.run(os.environ["TOKEN"])
