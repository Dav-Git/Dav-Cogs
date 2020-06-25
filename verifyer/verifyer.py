from redbot.core import commands, Config
import discord
from typing import Optional


class Verifyer(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=250620201622, force_registration=True)
        default_guild = {
            "text": "Welcome to [guild] please verify yourself to get access to the rest of the server by using ``[p]verify``.",
            "verifiedtext": "",
            "role": None,
            "memrole": None,
        }
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        text = await self.config.guild(member.guild).text()
        if text:
            await member.send(text)
        role = await self.config.guild(member.guild).role()
        if role:
            await member.add_roles(member.guild.get_role(role), reason="Verification required.")

    @commands.guild_only()
    @commands.command()
    async def verify(self, ctx, member: Optional[discord.Member]):
        if not member:
            member = ctx.author
        try:
            verifiedtext = self.config.guild(ctx.guild).verifiedtext()
            if verifiedtext:
                await member.send(verifiedtext)
        except discord.Forbidden:
            pass
        role = await self.config.guild(ctx.guild).role()
        if role:
            try:
                await member.remove_roles(
                    ctx.guild.get_role(role), reason="Member verified themselves."
                )
            except:
                pass
        memrole = await self.config.guild(ctx.guild).memrole()
        if memrole:
            await member.add_roles(
                ctx.guild.get_role(memrole), reason="Member verified themselves."
            )
        try:
            await ctx.message.remove()
        except:
            pass

    @commands.guild_only()
    @commands.group()
    async def verifyerset(self, ctx):
        """Settings for verifyer"""
        pass

    @commands.guild_only()
    @verifyerset.command()
    async def role(self, ctx, role: Optional[discord.Role]):
        """Set the role to assign to a user on guild join.\n\nLeave empty to disable this feature."""
        if not role:
            await self.config.guild(ctx.guild).role.set(None)
            await ctx.send("Verification role disabled.")
        else:
            await self.config.guild(ctx.guild).role.set(role.id)
            await ctx.send(f"Verification role set to {role.mention}.")

    @commands.guild_only()
    @verifyerset.command()
    async def message(self, ctx, text: Optional[str]):
        """Specify what message should be DMed to a user when they join the guild.\n\nLeave empty to disable this feature."""
        await self.config.guild(ctx.guild).text.set(text)
        await ctx.send(f"Message set to: ```{text}```")

    @commands.guild_only()
    @verifyerset.command()
    async def verifiedmessage(self, ctx, text: Optional[str]):
        """Specify what message should be DMed to a user when they verify themselves.\n\nLeave empty to disable this feature."""
        await self.config.guild(ctx.guild).verifiedtext.set(text)
        await ctx.send(f"Message set to: ```{text}```")

    @commands.guild_only()
    @verifyerset.command()
    async def memberrole(self, ctx, role: Optional[discord.Role]):
        """Set the role to assign to a user when they verify themselves.\n\nLeave empty to disable this feature."""
        if not role:
            await self.config.guild(ctx.guild).role.set(None)
            await ctx.send("Member role disabled.")
        else:
            await self.config.guild(ctx.guild).memrole.set(role.id)
            await ctx.send(f"Member role set to {role.mention}.")
