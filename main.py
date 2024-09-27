import attrs
import interactions
from interactions import listen, OptionType, slash_option, check, has_role, Embed, slash_command, SlashContext
import os
from interactions.api.events import MessageCreate
import colors
import config
from player_utils import Player, PlayersDB, translate_time, simple_time_transalte
import time
import datetime

AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = interactions.Client(token=token)
CHECK_ROLE = 1282491372250857676
BASE_PATH = os.path.join(os.getcwd())


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
@interactions.check(has_role(CHECK_ROLE))
async def handle_execute_command(ctx: interactions.SlashContext, channel: interactions.ChannelType, message: str):
    channel = await bot.fetch_channel(channel)
    if channel:
        await channel.send(message)
        await ctx.send("Command has been sent!", ephemeral=True)
    else:
        await ctx.send("Channel not found!", ephemeral=True)


@interactions.slash_command(
    name="test",
    description="Run Hard Coded Tests")
# @interactions.check(has_role(CHECK_ROLE))
async def handle_request_command(ctx: interactions.SlashContext):
    embed = Embed(
        description="Running Tests...",
        color=colors.DiscordColors.GREEN
    )
    msg = await ctx.send(embeds=embed)
    embed1 = Embed(
        description="Test Complete!",
        color=colors.DiscordColors.GREEN
    )
    await msg.edit(embeds=embed1)


@interactions.slash_command(
    name="unixtime",
    description="Convert time to unix timestamp. This command is a test command powered by Duckling."
)
@interactions.slash_option(
    name="time",
    description="Describe the time you want to convert. Example: 1d, 9/14/24, in one year, in 3 days, etc.",
    required=True,
    opt_type=OptionType.STRING
)
async def handle_unixtime_command(ctx: interactions.SlashContext, time):
    try:
        unix_timestamp = translate_time(time)
        await ctx.send(
            f"You asked for the Unix timestamp for the prompt '{time}'.\n This translates to <t:{unix_timestamp}:F> and has a unix timestamp of **{unix_timestamp}**.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@interactions.slash_command(
    name="blacklist",
    description="Add a user to the blacklist database.")
@interactions.slash_option(
    name="user",
    description="Who do you want to blacklist?",
    required=True,
    opt_type=OptionType.USER
)
@interactions.slash_option(
    name="blacklist_length",
    description="How long do you want to blacklist this user for?",
    required=True,
    opt_type=OptionType.STRING
)
@interactions.check(has_role(CHECK_ROLE))
async def handle_blacklist_command(ctx: interactions.SlashContext, user, blacklist_length):
    userobj = ctx.guild.get_member(user)
    user_roles = []
    for i in userobj.roles:
        user_roles.append(int(i.id))
    database = PlayersDB()
    if database.get_player(user.id):
        await ctx.send("This user is already blacklisted!")
        return
    user_id = user.id
    blacklist_until = translate_time(str(blacklist_length))
    new_player = Player(userid=user_id, roles=user_roles, blacklisted=True, blacklist_until=blacklist_until)
    database.save_player(new_player)
    await user.send(
        f"You have been blacklisted on Bonk Network! Your blacklist will expire <t:{blacklist_until}:R> on <t:{blacklist_until}:F>.")
    await ctx.send(f"Done! User <@{user_id}> is blacklisted until <t:{blacklist_until}:F>.")


bot.start()
