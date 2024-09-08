import interactions
from discord import Client
from discord.app_commands import guilds
from interactions import listen, OptionType, slash_option, check, has_role
import os
from interactions.api.events import MessageCreate
from tests.test_contexts import guild

import config
from player_class import Player, PlayersDB
import time

AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = interactions.Client(token=token, sync_interactions=True)


@listen()
async def on_ready():
    print("Bot has started with 0 commands, should clear bot.")
    print(bot.sync_interactions)


@interactions.slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: interactions.SlashContext):
    await ctx.send("Synced Bot.")


bot.start()
