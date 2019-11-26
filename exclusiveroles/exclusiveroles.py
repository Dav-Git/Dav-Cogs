import discord
from redbot.core import commands, checks


class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        role = after.guild.get_role(489455280266936321)
        if role not in before.roles:
            if role in after.roles:
                await after.remove_roles(after.guild.get_role(634692203582717990), reason="Active Applied")

                
    @commands.command()
    @checks.admin()
    async def retroscan(self, ctx):
        ctx.send("Retroscan started...")
        for user in ctx.guild.members:
            if ctx.guild.get_role(489455280266936321) in user.roles:
                if ctx.guild.get_role(634692203582717990) in user.roles:
                    await user.remove_roles(after.guild.get_role(634692203582717990), reason="Active Applied (RETROSCAN)")
        ctx.send("Retroscan completed.")
