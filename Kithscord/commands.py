import discord

import common
import user_commands
import admin_commands
from overload import *
import util


async def handle(cmd_str: str, invoker_msg: discord.Message, response_msg: discord.Message):
    args = cmd_str.split()

    is_admin = False
    for role in invoker_msg.author.roles:
        if role.id in common.ADMIN_ROLES:
            is_admin = True
            break

    try:
        if is_admin and args[0] in admin_cmds.keys():
            if len(args) - 1 in admin_cmds[args[0]].keys():
                await admin_cmds[args[0]][len(args) - 1](args[1:], invoker_msg, response_msg)
            elif -1 in admin_cmds[args[0]].keys():
                await admin_cmds[args[0]][-1](args[1:], invoker_msg, response_msg)

        elif args[0] in user_cmds.keys():
            if len(args) - 1 in user_cmds[args[0]].keys():
                await user_cmds[args[0]][len(args) - 1](args[1:], invoker_msg, response_msg)
            elif -1 in user_cmds[args[0]].keys():
                await user_cmds[args[0]][-1](args[1:], invoker_msg, response_msg)
            else:
                await util.edit_embed(response_msg, "Incorrect amount of argument(s)!", "")

        else:
            await util.edit_embed(response_msg, "Unknown command!", "")

    except Exception as exc:
        raise exc
