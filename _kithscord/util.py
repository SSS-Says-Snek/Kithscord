import asyncio
import io
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime

import aiohttp
import discord

import kithscord.common


async def pull_kithare(response, branch):
    """
    Pull and build Kithare from github
    """
    await kithscord.util.edit_embed(
        response,
        "Pulling and building Kithare",
        "Please wait while Kithare is being built",
        url_image="https://raw.githubusercontent.com/Kithare/"
        + "Kithscord/main/assets/fidget-spinner.gif",
    )

    if os.path.isdir("kithare"):
        shutil.rmtree("kithare")

    link = f"https://github.com/Kithare/Kithare/archive/{branch}.zip"
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as linkobj:
            resp = await linkobj.read()

    with zipfile.ZipFile(io.BytesIO(resp), 'r') as zipped:
        zipped.extractall()

    os.rename(f"Kithare-{branch}", "kithare")
    with open("kithare-buildlog.txt", "w") as f:
        proc = await asyncio.create_subprocess_shell(
            f"{sys.executable} {os.path.join('kithare', 'build.py')}",
            stdout=f,
            stderr=f,
        )

        for i in range(601):
            if proc.returncode is not None:
                break

            if i == 600:
                if proc.returncode is None:
                    proc.kill()
            await asyncio.sleep(1)

        f.write(f"\nProcess exited with exitcode {proc.returncode}")

    if proc.returncode:
        await kithscord.util.edit_embed(
            response,
            "Pulling and building Kithare",
            "Kithare Build Failed",
            0xFF0000
        )
        await response.reply(
            "Here is the buildlog for that, if you are interested",
            file=discord.File("kithare-buildlog.txt")
        )
    else:
        await kithscord.util.edit_embed(
            response,
            "Pulling and building Kithare",
            "Kithare Build Suceeded",
            0x00FF00
        )


def run_kcr(*args, timeout=5):
    """
    Run kcr command
    """
    # We are assuming that this code in run on a linux machine
    cmd = [os.path.join("kithare", "dist", "GCC-x64", "kcr")]
    cmd.extend(args)

    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        text=True,
    ).stdout


def log(msg: str):
    """
    Prints msg with the current time
    """
    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y %H:%M:%S')}] {msg}")


async def construct_embed(
        title, description, color=0xAAFFFF,
        url_image=None, url_thumbnail=None, fields=[]
):
    """
    Creates a discord.Embed with the provided arguments
    """
    embed = discord.Embed(title=title, description=description, color=color)

    if url_image:
        embed.set_image(url=url_image)
    if url_thumbnail:
        embed.set_thumbnail(url=url_thumbnail)
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2])

    return embed


async def edit_embed(
        message, title, description, color=0xAAFFFF,
        url_image=None, url_thumbnail=None, fields=[]
):
    """
    Edits the embed of a message with a much more tight function
    """
    embed = await construct_embed(
        title, description, color,
        url_image, url_thumbnail, fields
    )
    return await message.edit(embed=embed)


async def send_embed(
        channel, title, description, color=0xAAFFFF,
        url_image=None, url_thumbnail=None, fields=[]
):
    """
    Sends an embed with a much more tight function
    """
    return await channel.send(embed=await construct_embed(
        title, description, color,
        url_image, url_thumbnail, fields
    ))


def code_block(string: str, max_characters=2048):
    """
    Formats text into discord code blocks
    """
    string = string.replace("```", "\u200b`\u200b`\u200b`\u200b")
    max_characters -= 7

    if len(string) > max_characters:
        return f"```\n{string[:max_characters - 7]} ...```"
    else:
        return f"```\n{string[:max_characters]}```"


def escape(message: str):
    """
    Converts normal string into "discord" string that includes backspaces 
    to cancel out unwanted changes
    """
    if '\\' in message:
        message = message.replace('\\', r'\\')
    if '*' in message:
        message = message.replace('*', r'\*')
    if '`' in message:
        message = message.replace('`', r'\`')
    if '_' in message:
        message = message.replace('_', r'\_')
    return message
