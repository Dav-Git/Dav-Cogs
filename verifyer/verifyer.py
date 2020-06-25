from redbot.core import commands, Config
import discord
from typing import Optional
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Verifyer", __file__)


@cog_i18n(_)
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
            await member.add_roles(member.guild.get_role(role), reason=_("Verification required."))

    @commands.guild_only()
    @commands.command()
    async def verify(self, ctx, member: Optional[discord.Member]):
        if not member:
            member = ctx.author
        try:
            verifiedtext = await self.config.guild(ctx.guild).verifiedtext()
            if verifiedtext:
                await member.send(verifiedtext)
        except discord.Forbidden:
            pass
        role = await self.config.guild(ctx.guild).role()
        if role:
            try:
                await member.remove_roles(
                    ctx.guild.get_role(role), reason=_("Member verified themselves.")
                )
            except:
                pass
        memrole = await self.config.guild(ctx.guild).memrole()
        if memrole:
            await member.add_roles(
                ctx.guild.get_role(memrole), reason=_("Member verified themselves.")
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
            await ctx.send_help()
            await ctx.send(_("Verification role disabled."))
        else:
            await self.config.guild(ctx.guild).role.set(role.id)
            await ctx.send(
                _("Verification role set to {rolemention}.").format(rolemention=role.mention)
            )

    @commands.guild_only()
    @verifyerset.command()
    async def message(self, ctx, *, text: Optional[str]):
        """Specify what message should be DMed to a user when they join the guild.\n\nLeave empty to disable this feature."""
        await self.config.guild(ctx.guild).text.set(text)
        await ctx.send(_("Message set to: ```{text}```").format(text=text))

    @commands.guild_only()
    @verifyerset.command()
    async def verifiedmessage(self, ctx, *, text: Optional[str]):
        """Specify what message should be DMed to a user when they verify themselves.\n\nLeave empty to disable this feature."""
        await self.config.guild(ctx.guild).verifiedtext.set(text)
        await ctx.send(_("Message set to: ```{text}```").format(text=text))

    @commands.guild_only()
    @verifyerset.command()
    async def memberrole(self, ctx, role: Optional[discord.Role]):
        """Set the role to assign to a user when they verify themselves.\n\nLeave empty to disable this feature."""
        if not role:
            await self.config.guild(ctx.guild).role.set(None)
            await ctx.send_help()
            await ctx.send(_("Member role disabled."))
        else:
            await self.config.guild(ctx.guild).memrole.set(role.id)
            await ctx.send(_("Member role set to {rolemention}.").format(rolemention=role.mention))
