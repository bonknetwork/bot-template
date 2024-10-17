from interactions import listen
from bot_instance import bot  # Import bot and role_check from bot_instance
import os
for i in os.listdir("commands"):
    if i.endswith(".py"):
        exec(f"from commands.{i.replace('.py', '')} import *")

@listen()
async def on_ready():
    print("Bot has started.")

# Start the bot
bot.start()
