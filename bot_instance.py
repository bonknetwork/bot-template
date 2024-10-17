from utils import config
from interactions import Client, check, SlashContext

# Get Bonk Network bot token and create bot client
AppConfig_obj = config.AppConfig()
token = AppConfig_obj.get_bonk_staff_key()
bot = Client(token=token)

CHECK_ROLES = [1282491372250857676, 1263837661605527603, 1259828028012232714]

# Role check decorator for role-specific commands
def role_check():
    async def predicate(ctx: SlashContext):
        user_roles = [int(i.id) for i in ctx.author.roles]
        return any(role_id in user_roles for role_id in CHECK_ROLES)
    return check(predicate)
