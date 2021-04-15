import sys

import discord

import util
from user_commands import UserCommand


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
        await util.edit_embed(
            self.response,
            "Stopping bot...",
            "I gotta go now, but I will BRB"
        )
        sys.exit(0)
