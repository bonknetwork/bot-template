from interactions import slash_command, SlashContext, Embed
from utils import colors


@slash_command(name="help", description="Help command.")
async def handle_help_command(ctx: SlashContext):
    embed = Embed(
        description="This bot is still in development. Please check back later for a response from this command!",
        color=colors.DiscordColors.GREEN
    )
    await ctx.send(embeds=embed)
