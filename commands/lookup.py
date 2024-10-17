from interactions import slash_command, slash_option, OptionType, SlashContext, Embed
from utils import colors
from utils.command_utils import PlayersDB
from json.encoder import INFINITY
from bot_instance import role_check  # Import role_check from bot_instance

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

    role_names = {ctx.guild.get_role(role_id).name for role_id in player.roles}

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
