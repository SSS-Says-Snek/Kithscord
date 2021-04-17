import os
import sys

import discord

import kithscord.util
from kithscord.user_commands import UserCommand


class AdminCommand(UserCommand):
    """
    Base class to handle admin commands.
    """
    async def cmd_error(self):
        """
        Temporary
        """
        raise ValueError("Bruh")

    async def cmd_sudo(self):
        """
        Implement kh!sudo, for admins to send messages via the bot
        """
        await self.invoke_msg.channel.send(self.string)
        await self.response.delete()
        await self.invoke_msg.delete()

    async def cmd_stop(self):
        """
        Implement kh!stop, for admins to stop the bot
        """
        self.check_args(0)
        await kithscord.util.edit_embed(
            self.response,
            "Stopping bot...",
            "I gotta go now, but I will BRB"
        )
        sys.exit(0)

    async def cmd_pull(self):
        """
        Implement kh!pull, to pull and build kithare
        """
        self.check_args(0, 2)
        if not self.args:
            self.args.append("main")

        await kithscord.util.pull_kithare(
            self.args[0], self.response, len(self.args) == 2
        )
