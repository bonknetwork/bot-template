import time
from utils import colors, config
from interactions import (
    Client, listen, OptionType, check, Embed, slash_command, SlashContext,
    slash_option, ChannelType
)
from utils.command_utils import Player, PlayersDB, translate_time
from json.encoder import INFINITY


# Get Bonk Network bot token and create bot client
AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = Client(token=token)

CHECK_ROLES = [1282491372250857676, 1263837661605527603, 1259828028012232714]


@listen()
async def on_ready():
    print("Bot has started.")


# Role check decorator for role-specific commands
def role_check():
    async def predicate(ctx: SlashContext):
        user_roles = [int(i.id) for i in ctx.author.roles]
        return any(role_id in user_roles for role_id in CHECK_ROLES)
    return check(predicate)


@slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: SlashContext):
    embed = Embed(
        description="This bot is still in development. Please check back later for a response from this command!",
        color=colors.DiscordColors.GREEN
    )
    await ctx.send(embeds=embed)


@slash_command(name="say", description="Send a message in a specified channel.")
@slash_option(
    name="channel",
    description="Where would you like to send the message?",
    required=True,
    opt_type=OptionType.CHANNEL
)
@slash_option(
    name="message",
    description="What message would you like to send?",
    required=True,
    opt_type=OptionType.STRING
)
@role_check()
async def handle_say_command(ctx: SlashContext, channel: ChannelType, message: str):
    channel = await bot.fetch_channel(channel)
    if channel:
        await channel.send(message)
        await ctx.send("Command has been successfully sent!", ephemeral=True)
    else:
        await ctx.send("Channel not found!", ephemeral=True)


@slash_command(name="dm", description="Send a direct message as the bot.")
@slash_option(
    name="user",
    description="Who do you want to send the message to?",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="message",
    description="What message would you like to send?",
    required=True,
    opt_type=OptionType.STRING
)
@role_check()
async def handle_dm_command(ctx: SlashContext, user, message: str):
    user = ctx.guild.get_member(user)
    embed = Embed(description=message, color=colors.DiscordColors.BLUE)
    await user.send(embeds=embed)
    await ctx.send(f"DM sent to {user.display_name}!\nMessage contents: {message}", ephemeral=True)


@slash_command(name="test", description="Run predefined tests.")
async def handle_test_command(ctx: SlashContext):
    test_start_msg = Embed(description="Running Tests...", color=colors.DiscordColors.GREEN)
    msg = await ctx.send(embeds=test_start_msg)
    test_complete_msg = Embed(description="Test Complete!", color=colors.DiscordColors.GREEN)
    await msg.edit(embeds=test_complete_msg)


@slash_command(name="unixtime", description="Convert time to a Unix timestamp.")
@slash_option(
    name="time",
    description="Describe the time you want to convert (e.g., '1d', '9/14/24', 'in one year').",
    required=True,
    opt_type=OptionType.STRING
)
async def handle_unixtime_command(ctx: SlashContext, time_str: str):
    try:
        unix_timestamp = translate_time(time_str)
        unix_msg = Embed(
            description=f"Unix timestamp for '{time_str}':\n**<t:{unix_timestamp}:F>** (Unix: **{unix_timestamp}**).",
            color=colors.DiscordColors.BLUE
        )
        await ctx.send(embeds=unix_msg)
    except Exception as e:
        error_msg = Embed(description=f"An error occurred: {e}", color=colors.DiscordColors.RED)
        await ctx.send(embeds=error_msg)


@slash_command(name="lookup", description="Look up a user in the database.")
@slash_option(
    name="user",
    description="Which user would you like to look up?",
    required=True,
    opt_type=OptionType.USER
)
@role_check()
async def handle_lookup_command(ctx: SlashContext, user):
    user = ctx.guild.get_member(user)
    database = PlayersDB()
    user_id = user.id
    player = database.get_player(user_id)

    if not player:
        await ctx.send(
            embeds=Embed(description="This user is not in the database!", color=colors.DiscordColors.RED)
        )
        return

    # Retrieve user roles
    role_names = {ctx.guild.get_role(role_id).name for role_id in player.roles}

    # Build description for the embed
    desc_text = (
        f"**User ID:** {user_id}\n\n"
        f"**Roles:**\n" + "\n".join(f"- {role}" for role in role_names) +
        f"\n\n**Blacklisted:** {player.blacklisted}\n"
        f"**Blacklist Until:** " + (
            "Permanent" if player.blacklist_until == INFINITY else f"<t:{player.blacklist_until}:F>"
        ) +
        f"\n\n**Blacklist Reason:** {player.blacklist_reason}\n**IGN:** {player.ign}"
    )
    embed = Embed(title=f"Player Lookup: {user.username}", description=desc_text, color=colors.DiscordColors.GOLD)
    await ctx.send(embeds=embed)


@slash_command(name="blacklist", description="Add a user to the blacklist.")
@slash_option(
    name="user",
    description="Which user would you like to blacklist?",
    required=True,
    opt_type=OptionType.USER
)
@slash_option(
    name="blacklist_length",
    description="For how long would you like to blacklist this user?",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="reason",
    description="Please provide a reason for blacklisting this user.",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="ign",
    description="Provide the user's in-game name (IGN). This is case sensitive.",
    required=False,
    opt_type=OptionType.STRING
)
@role_check()
async def handle_blacklist_command(ctx: SlashContext, user, blacklist_length, reason=None, ign=None):
    user_obj = ctx.guild.get_member(user)
    user_roles = [int(role.id) for role in user_obj.roles]
    database = PlayersDB()
    user_id = user.id

    # Check if user is already blacklisted
    if database.get_player(user_id):
        await ctx.send(
            embeds=Embed(
                title="User Already Blacklisted",
                description=f"The user <@{user_id}> is already blacklisted.",
                color=colors.DiscordColors.RED
            ),
            ephemeral=True
        )
        return

    # Parse blacklist length
    try:
        blacklist_until = translate_time(str(blacklist_length))
    except:
        await ctx.send(
            embeds=Embed(
                title="Invalid Time Format",
                description="The time format is invalid. Please use `1d`, `1w`, `1mo`, or a specific date.",
                color=colors.DiscordColors.RED,
                footer="Error: Please try again."
            ),
            ephemeral=True
        )
        return

    reason = reason or "No specific reason provided."
    ign = ign or "No IGN provided."

    # Validate blacklist time
    if blacklist_until != INFINITY and blacklist_until < time.time():
        await ctx.send(
            embeds=Embed(
                title="Invalid Blacklist Time",
                description="The blacklist time cannot be in the past. Please set a future date.",
                color=colors.DiscordColors.RED
            ),
            ephemeral=True
        )
        return

    # Save player to database
    new_player = Player(
        userid=user_id,
        roles=user_roles,
        blacklisted=True,
        blacklist_until=blacklist_until,
        blacklist_reason=reason,
        ign=ign
    )
    database.save_player(new_player)

    # Notify user via DM
    if blacklist_until == INFINITY:
        dm_message = (
            f"**You have been permanently blacklisted from Bonk Network.**\n\n"
            f"**Reason:** {reason}\n"
            f"**IGN:** {ign}\n\n"
            "This blacklist is permanent and will not expire. You are also ineligible for server positions such as staff or developer."
        )
    else:
        dm_message = (
            f"**You have been blacklisted from Bonk Network.**\n\n"
            f"**Reason:** {reason}\n"
            f"**IGN:** {ign}\n\n"
            f"Your blacklist will expire <t:{blacklist_until}:R> on **<t:{blacklist_until}:F>**. "
            "During this time, you are not eligible for server positions such as staff or developer."
        )

    try:
        await user.send(embeds=Embed(title="Blacklist Notification", description=dm_message, color=colors.DiscordColors.RED))
    except:
        await ctx.send(
            embeds=Embed(title="DM Failed", description=f"Failed to send DM to <@{user_id}>.", color=colors.DiscordColors.RED), ephemeral=True
        )

    # Confirm action
    if blacklist_until == INFINITY:
        await ctx.send(
            embeds=Embed(title="Blacklist Action Completed", description=f"User <@{user_id}> has been permanently blacklisted.", color=colors.DiscordColors.GREEN)
        )
    else:
        await ctx.send(
            embeds=Embed(title="Blacklist Action Completed", description=f"User <@{user_id}> has been blacklisted until <t:{blacklist_until}:F>.", color=colors.DiscordColors.GREEN)
        )


# Start the bot
bot.start()
