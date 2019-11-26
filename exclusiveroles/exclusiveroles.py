import discord
from redbot.core import commands


class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""
    
    def __init__(self, bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        role=after.guild.get_role(489455280266936321)
        if not role in before.roles:
            if role in after.roles:
                await after.remove_roles(after.guild.get_roles(634692203582717990),reason="Active Applied")
        return
