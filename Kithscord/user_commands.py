import discord

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
                title = "An exception occured while handling the command!"
                msg = util.code_block(
                    f"{type(exc).__name__}: {', '.join(map(str, exc.args))}"
                )

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
        await util.edit_embed(self.response, "Version", "69.69")
