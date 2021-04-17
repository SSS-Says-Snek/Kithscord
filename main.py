import os

import discord

from kithscord import commands, common, util


@common.bot.event
async def on_ready():
    """
    The initial start when Kithscord gets booted.
    """
    util.log("Kithscord ready!")

    if not os.path.isdir("kithare"):
        print("Kithare installation not detected, installing kithare")
        await util.pull_kithare()
        print("Finished installing Kithare")


@common.bot.event
async def on_message(msg: discord.Message):
    """
    When a message is sent.
    """
    if msg.author.bot:
        return

    if msg.content.startswith(common.PREFIX):
        cmd = commands.UserCommand()
        for role in msg.author.roles:
            if role.id in common.ADMIN_ROLES:
                cmd = commands.AdminCommand()
                break

        response = await util.send_embed(
            msg.channel, "", "Your command is being processed!"
        )
        await cmd.handle_cmd(msg, response)

if __name__ == "__main__":
    common.bot.run(os.environ["TOKEN"])
