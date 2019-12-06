import discord
from redbot.core import commands, checks


class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild.id == 332834024831582210:
            role = after.guild.get_role(489455280266936321)
            if role not in before.roles:
                if role in after.roles:
                    await after.remove_roles(after.guild.get_role(634692203582717990), reason="Active Applied")
        elif after.guild.id == 443031049111601152:
            role = after.guild.get_role(645349225898573854)
            if role not in before.roles:
                if role in after.roles:
                    await after.remove_roles(after.guild.get_role(443075487326273536), reason="CincinationMember Applied")

                
    @commands.command()
    @checks.admin()
    async def retroscan(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. Removes the second role if both roles are present on a user. """
        
        if not isinstance(role1, discord.Role) or not isinstance(role2, discord.Role) :
            return await ctx.send("You need to provide at least 2 roles")
        
        else:
            await ctx.send("\n`Retroscan started...`\n")
            for user in ctx.guild.members:
                if role1 in user.roles:
                    if role2 in user.roles:
                        await user.remove_roles(role2, reason="Exclusive Role(RETROSCAN)")
            await ctx.send("\n`Retroscan completed.`\n")
