import os
import traceback

import discord

import kithscord.common
import kithscord.util


class ArgError(Exception):
    pass


class UserCommand:
    """
    Base class to handle user commands.
    """

    def __init__(self):
        """
        Initialise UserCommand class
        """
        # Create a dictionary of command names and respective handler functions
        self.cmds_and_funcs = {}
        for i in dir(self):
            if i.startswith("cmd_"):
                self.cmds_and_funcs[i[len("cmd_"):]] = self.__getattribute__(i)

        # Avoid PyCharm shouting that member variables can't be declared
        # outside __init__
        self.invoke_msg = None
        self.response = None
        self.args = None
        self.string = None

    async def handle_cmd(
        self, invoke_msg: discord.Message, resp_msg: discord.Message
    ):
        """
        Calles the appropriate sub function to handle commands.
        Must return True on successful command execution, False otherwise
        """
        self.invoke_msg = invoke_msg
        self.response = resp_msg

        cmd_str = invoke_msg.content[len(kithscord.common.PREFIX):].strip()
        self.args = cmd_str.split()
        cmd = self.args.pop(0)
        self.string = cmd_str[len(cmd):].strip()

        kithscord.util.log(
            f"Command invoked by {invoke_msg.author}: {cmd_str}"
        )

        try:
            await self.cmds_and_funcs[cmd]()

        except Exception as exc:
            if isinstance(exc, ArgError):
                title = "Incorrect amount of argument(s)!"
                msg = exc.args[0]

            elif isinstance(exc, KeyError):
                title = "Unrecognized command!"
                msg = ""

            else:
                error_tuple = (type(exc), exc, exc.__traceback__)
                title = "An exception occured while handling the command!"
                msg = kithscord.util.code_block(
                    ''.join(traceback.format_exception(*error_tuple)).strip()
                )

            await kithscord.util.edit_embed(resp_msg, title, msg, 0xFF0000)

    def check_args(self, minarg, maxarg=None):
        """
        A utility for a function to check that the correct number of args were
        passed
        """
        exp = f"between {minarg} and {maxarg}"
        if maxarg is None:
            exp = maxarg = minarg

        got = len(self.args)
        if not (minarg <= got <= maxarg):
            raise ArgError(
                f"The number of arguments must be {exp} but {got} were given"
            )

    async def cmd_version(self):
        """
        Implement kh!version, for check version
        """
        self.check_args(0)
        await kithscord.util.edit_embed(
            self.response,
            "Version",
            kithscord.util.run_kcr('-v')
            + f"Kithscord Version {kithscord.common.VERSION}"
        )

    async def cmd_lex(self):
        """
        Implement kh!lex, to lex kithare source
        """
        code = self.string.strip().strip('`')
        with open("tempfile", "w") as f:
            f.write(code)

        try:
            await kithscord.util.edit_embed(
                self.response,
                "Lexed Kithare output",
                kithscord.util.code_block(
                    kithscord.util.run_kcr("--lex", "tempfile")
                )
            )
        finally:
            os.remove("tempfile")
