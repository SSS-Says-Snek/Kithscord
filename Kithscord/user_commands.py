import discord

import traceback

import util
import common


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

        # Avoid PyCharm shouting that member variables can't be declared outside __init__
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

        cmd_str = invoke_msg.content[len(common.PREFIX):].strip()
        self.args = cmd_str.split()
        cmd = self.args.pop(0)
        self.string = cmd_str[len(cmd):].strip()

        try:
            await self.cmds_and_funcs[cmd]()
            await util.log(f"Command invoked by {invoke_msg.author}: {cmd_str}")

        except Exception as exc:
            if isinstance(exc, ArgError):
                title = "Incorrect amount of argument(s)!"
                msg = exc.args[0]

            elif isinstance(exc, KeyError):
                title = "Unrecognized command!"
                msg = ""

            else:
                # redacted_path = None TODO: Figure out heroku path
                error_tuple = (type(exc), exc, exc.__traceback__)
                title = "An exception occured while handling the command!"
                msg = util.code_block(''.join(traceback.format_exception(*error_tuple)).strip())

            await util.edit_embed(resp_msg, title, msg, 0xFF0000)

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
        self.check_args(0)
        await util.edit_embed(self.response, "Version", "Kithare Version: 0.0.0\n"
                                                        "Kithscord Version: 69.69")
