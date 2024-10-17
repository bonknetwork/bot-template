from interactions import slash_command, SlashContext, Embed
from utils import colors


@slash_command(name="test", description="Run predefined tests.")
async def handle_test_command(ctx: SlashContext):
    test_start_msg = Embed(description="Running Tests...", color=colors.DiscordColors.GREEN)
    msg = await ctx.send(embeds=test_start_msg)
    test_complete_msg = Embed(description="Test Complete!", color=colors.DiscordColors.GREEN)
    await msg.edit(embeds=test_complete_msg)
