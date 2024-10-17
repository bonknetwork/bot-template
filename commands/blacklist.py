from interactions import slash_command, slash_option, OptionType, SlashContext, Embed
from utils import colors
import time
from utils.command_utils import Player, PlayersDB, translate_time
from json.encoder import INFINITY
from bot_instance import role_check  # Import role_check from bot_instance

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

    new_player = Player(
        userid=user_id,
        roles=user_roles,
        blacklisted=True,
        blacklist_until=blacklist_until,
        blacklist_reason=reason,
        ign=ign
    )
    database.save_player(new_player)

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

    if blacklist_until == INFINITY:
        await ctx.send(
            embeds=Embed(title="Blacklist Action Completed", description=f"User <@{user_id}> has been permanently blacklisted.", color=colors.DiscordColors.GREEN)
        )
    else:
        await ctx.send(
            embeds=Embed(title="Blacklist Action Completed", description=f"User <@{user_id}> has been blacklisted until <t:{blacklist_until}:F>.", color=colors.DiscordColors.GREEN)
        )
