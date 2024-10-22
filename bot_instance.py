from utils import config
from interactions import Client, check, SlashContext
import os

# Get Bonk Network bot token and create bot client
AppConfig_obj = config.AppConfig()
in_codespace = False
if in_codespace:
    config_dir = os.getcwd()
    config_dir = os.join(config_dir, "utils")
else:
    config_dir = None
token = AppConfig_obj.get_bonk_staff_key(config_dir=config_dir)
bot = Client(token=token)

CHECK_ROLES = [1282491372250857676, 1263837661605527603, 1259828028012232714]

# Role check decorator for role-specific commands
def role_check():
    async def predicate(ctx: SlashContext):
        user_roles = [int(i.id) for i in ctx.author.roles]
        return any(role_id in user_roles for role_id in CHECK_ROLES)
    return check(predicate)
