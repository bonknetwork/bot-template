from interactions import slash_command, slash_option, OptionType, ChannelType, SlashContext
from bot_instance import bot, role_check

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
