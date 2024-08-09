import interactions
from interactions import listen, OptionType, slash_option, check, has_role
import os
from interactions.api.events import MessageCreate
import config
import time

AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = interactions.Client(token=token)

@listen()
async def on_ready():
    #await bot.clear_application_commands()
    print("Bot has started.")

@interactions.slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: interactions.SlashContext):
    await ctx.send(
        "This bot is still in development. Please check back later for a response from this command!", ephemeral=True)

@interactions.slash_command(
    name="execute",
    description="Run a Console Command")
@interactions.check(has_role(1263838065047109642))
@interactions.slash_option(
    name="command",
    description="What command do you want to run?",
    required=True,
    opt_type=OptionType.STRING
)

async def handle_execute_command(ctx: interactions.SlashContext, command: str):
    channel = await bot.fetch_channel(1271152792207229081)
    if channel:
        await channel.send(command)
        await ctx.send("Message sent successfully!")
    else:
        await ctx.send("Channel not found!")

@interactions.slash_command(
    name="test",
    description="Make a moderation request.")
@interactions.check(has_role(1263838065047109642))

async def handle_request_command(ctx: interactions.SlashContext):
    await ctx.send("Running Tests...")
    #await bot.sync_commands()
    await ctx.send("Test Complete!")

bot.start()