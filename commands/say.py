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
    message1 = """@everyone
After much thought and consideration, we have made the difficult decision to officially close Bonk Network. This decision wasn’t easy, as Bonk Network has been more than just a Minecraft server—it has been a home for creativity, friendship, and community. However, ongoing challenges, including management issues, hosting problems, and repeated attacks, have made it increasingly difficult to sustain the server. These issues have hindered its performance and prevented us from delivering the experience we always envisioned.
    
One of the hardest realizations for us was that we fell short of our original goals, like maintaining a no pay-to-win environment and offering a mainly vanilla experience. These goals were incredibly important to us, but the high cost of hosting and the need to sustain the server financially led us to make compromises we never wanted to make. Although the store was essential for survival, it ultimately clashed with the principles we started with.

This is a deeply personal decision for me and the team, as we poured our hearts and countless hours into this server to make it the best it could be. We truly loved Bonk Network, and it has been amazing to see the friendships and memories that have grown out of this community. Saying goodbye is painful, but we know this is the right step forward.

As we prepare to close, we want to make sure everyone is aware of the following:

- Refunds: We will be refunding any purchases made on our store within the past three days. Please reach out if you have any questions or concerns about the process.\n
- Community Transition: To keep our incredible community connected, we encourage everyone to join this new Discord server. If you are currently boosting Bonk Network, we kindly ask that you stop boosting and consider supporting the new server instead with your boosts ( <@1232077982915629088> ). https://discord.gg/bNASWF5KcS

"""
    message2 = """Before we officially say goodbye, we want to celebrate everything we’ve accomplished together. We will be hosting a FINAL Dragon Fight, complete with fun twists and surprises, as a sendoff for Bonk Network. This event will be a way for us to come together one last time and make an unforgettable memory. Stay tuned for details—we hope to see as many of you there as possible!

We are so grateful for every single person who joined Bonk Network, supported it, and helped it grow into what it became. Thank you for being part of this journey. While it’s sad to see Bonk Network come to an end, we hope the friendships and experiences we’ve shared here will last far beyond the server itself.

Special thanks to our amazing staff team for their dedication and hard work. We couldn’t have done it without you!
Most of all, special thanks to <@787443433949364274> for founding Bonk Network and making it what was today. ❤️

Stay tuned for more information about the final Dragon Fight and the new server! We hope to see you there! (Here's the link again: https://discord.gg/bNASWF5KcS)

Sincerely,
<@787443433949364274>, <@627980371887128606>, <@823603369230467073>, The Bonk Network Team and it's staff, now or in the past.
"""
    if channel:
        await channel.send(message1)
        await channel.send(message2)
        await ctx.send("Command has been successfully sent!", ephemeral=True)
    else:
        await ctx.send("Channel not found!", ephemeral=True)
