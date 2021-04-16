import os

import discord
from dotenv import load_dotenv

if os.path.isfile(".env"):
    load_dotenv()  # take environment variables from .env

bot = discord.Client()

ADMIN_ROLES = {819457027776446494, 810843243071143946, 830567257272877126}
PREFIX = "kh!"

VERSION = "v0.1.1"
