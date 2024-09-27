import interactions
from discord import Client
from discord.app_commands import guilds
from interactions import listen, OptionType, slash_option, check, has_role, sync_needed
import os
from interactions.api.events import MessageCreate
from tests.test_contexts import guild
import discord
import config
from player_utils import Player, PlayersDB
import time

AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = interactions.Client(token=token, sync_interactions=True)


@listen()
async def on_ready():
    print(f"Bot has started with 0 commands, should clear bot.")


@interactions.slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: interactions.SlashContext):
    await ctx.send("E")


bot.start()
