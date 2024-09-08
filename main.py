import interactions
from interactions import listen, OptionType, slash_option, check, has_role
import os
from interactions.api.events import MessageCreate
import config
from player_class import Player, PlayersDB
import time

AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = interactions.Client(token=token)
BONK_STAFF_DEV_ROLE = 1263838065047109642


def has_any_role(role_ids):
    async def predicate(ctx: interactions.CommandContext):
        member = ctx.author
        if isinstance(member, interactions.Member):
            return any(role.id in role_ids for role in member.roles)
        return False

    return interactions.check(predicate)


@listen()
async def on_ready():
    print("Bot has started.")


@interactions.slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: interactions.SlashContext):
    await ctx.send("This bot is still in development. Please check back later for a response from this command!")


@interactions.slash_command(
    name="say",
    description="say something in a channel")
@interactions.slash_option(
    name="channel",
    description="where do you want to send it",
    required=True,
    opt_type=OptionType.CHANNEL
)
@interactions.slash_option(
    name="message",
    description="what do you want to say",
    required=True,
    opt_type=OptionType.STRING
)
async def handle_execute_command(ctx: interactions.SlashContext, channel: interactions.ChannelType, message: str):
    required_roles = [BONK_STAFF_DEV_ROLE]
    user_roles = {role.id for role in ctx.author.roles}
    has_role_perms = False
    for i in required_roles:
        if i in user_roles:
            has_role_perms = True
    if has_role_perms:
        channel = await bot.fetch_channel(channel)
        if channel:
            await channel.send(message)
            await ctx.send("Command has been sent!", ephemeral=True)
        else:
            await ctx.send("Channel not found!", ephemeral=True)
    else:
        await ctx.send("You do not have permission to run this command!", ephemeral=True)


@interactions.slash_command(
    name="test",
    description="Run Hard Coded Tests")
@interactions.check(has_role(BONK_STAFF_DEV_ROLE))
async def handle_request_command(ctx: interactions.SlashContext):
    await ctx.send("Running Tests...")
    ban_log_channel = 1259602927509835818
    channel = await bot.fetch_channel(ban_log_channel)
    message = "This is a test ban log, please ignore this."
    await handle_execute_command(ctx, channel, message)
    await ctx.send("Test Complete!")

"""
@interactions.slash_command(
    name="blacklist",
    description="Add a user to the blacklist database.")
@interactions.slash_option(
    name="user",
    description="Who do you want to blacklist?",
    required=True,
    opt_type=OptionType.USER
)
async def handle_execute_command(ctx: interactions.SlashContext, user):
    database = PlayersDB()
    new_player = Player(userid=int(user.id), roles=list(user.roles))
    database.save_player((new_player))
    await ctx.send("Done!", ephemeral=True)



@interactions.slash_command(
    name="execute",
    description="Run a Console Command")
@interactions.slash_option(
    name="command",
    description="What command do you want to run?",
    required=True,
    opt_type=OptionType.STRING
)
async def handle_execute_command(ctx: interactions.SlashContext, command: str):
    required_roles = [BONK_STAFF_DEV_ROLE]
    user_roles = {role.id for role in ctx.author.roles}
    has_role_perms = False
    for i in required_roles:
        if i in user_roles:
            has_role_perms = True
    if has_role_perms:
        channel = await bot.fetch_channel(1271152792207229081)
        if channel:
            await channel.send(command)
            await ctx.send("Command has been sent!", ephemeral=True)
        else:
            await ctx.send("Channel not found!", ephemeral=True)
    else:
        await ctx.send("You do not have permission to run this command!", ephemeral=True)
"""

bot.start()
