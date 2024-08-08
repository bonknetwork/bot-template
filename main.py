import interactions
from interactions import listen, OptionType, slash_option, check, has_role
import os
from interactions.api.events import MessageCreate
import config
import json_tools

AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_bot_key()
bot = interactions.Client(token=token)

@listen()
async def on_ready():
    print("Bot has started.")

@interactions.slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: interactions.SlashContext):
    await ctx.send(
        "This bot is still in development. Please check back later for a response from this command!", ephemeral=True)

@interactions.slash_command(
    name="test",
    description="Make a moderation request.")
@interactions.check(has_role(1242197189048930314))
@interactions.slash_option(
    name="request",
    description="What do you request?",
    required=True,
    opt_type=OptionType.STRING
)
async def handle_request_command(ctx: interactions.SlashContext, request: str):
    await ctx.send("Request send with the following ".format(request), ephemeral=True)
    requests_dict = json_tools.load_json("mod-requests.json")
    requests_dict[ctx.author.id] = request
    json_tools.save_json("mod-requests.json", requests_dict)

bot.start()