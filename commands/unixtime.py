from interactions import slash_command, slash_option, OptionType, SlashContext, Embed
from utils import colors
from utils.command_utils import translate_time


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
