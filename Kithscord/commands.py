import discord

import common
import user_commands
import admin_commands
from overload import *
import util


async def handle(cmd_str: str, invoker_msg: discord.Message, response_msg: discord.Message):
    args = cmd_str.split()
    arg_length = len(args) - 1

    is_admin = False
    for role in invoker_msg.author.roles:
        if role.id in common.ADMIN_ROLES:
            is_admin = True
            break

    if arg_length == -1:
        return

    try:
        if is_admin and args[0] in admin_cmds.keys():
            overloads = admin_cmds[args[0]]

            if arg_length in overloads.keys():
                await overloads[arg_length](args[1:], invoker_msg, response_msg)
                return
            elif -1 in overloads.keys():
                await overloads[-1](args[1:], invoker_msg, response_msg)
                return

        if args[0] in user_cmds.keys():
            overloads = user_cmds[args[0]]

            if arg_length in overloads.keys():
                await overloads[arg_length](args[1:], invoker_msg, response_msg)
            elif -1 in overloads.keys():
                await overloads[-1](args[1:], invoker_msg, response_msg)
            else:
                await util.edit_embed(response_msg, "Incorrect amount of argument(s)!", "")

        else:
            await util.edit_embed(response_msg, "Unknown command!", "")

    except Exception as exc:
        raise exc
