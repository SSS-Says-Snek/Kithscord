import os
import sys

import discord

import kithscord.util
from kithscord.user_commands import UserCommand

ispulling = False


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
        global ispulling
        self.check_args(0, 1)
        if not self.args:
            self.args.append("main")

        if ispulling:
            await kithscord.util.edit_embed(
                self.response,
                "Pull and build failed",
                "You cannot pull while another pull operation is running",
                0xFF0000
            )
            return

        ispulling = True
        try:
            await kithscord.util.pull_kithare(self.response, self.args[0])
        finally:
            ispulling = False
            if os.path.isfile("kithare-buildlog.txt"):
                os.remove("kithare-buildlog.txt")
