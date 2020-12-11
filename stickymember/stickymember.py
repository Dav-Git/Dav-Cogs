from redbot.core import commands, Config, checks
from discord import Member, Forbidden

from redbot.core.i18n import cog_i18n, Translator
from logging import getLogger

from typing import Union

_ = Translator("StickyMember", __file__)


@cog_i18n(_)
class StickyMember(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, 231215102020, force_registration=True)
        default = {"roles": [], "active": False}
        self.config.register_member(**default)
        self.logger = getLogger("red.cog.dav-cogs.stickymember")

    async def red_delete_data_for_user(self, *, requester, user_id):
        data = self.config.all_members()
        for g in data:
            for m in g:
                if m == user_id:
                    await self.config.member_from_ids(g, m).clear()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if await self.config.member(after).active():
            role_ids = [r.id for r in after.roles]
            role_ids.remove(after.guild.id)
            await self.config.member(after).roles.set(role_ids)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.config.member(member).active():
            try:
                await member.add_roles(
                    *[member.guild.get_role(r) for r in await self.config.member(member).roles()]
                )
            except Forbidden:
                self.logger.warn("Couldn't assign roles to {member.id} on rejoin. 403")

    @checks.admin()
    @commands.command()
    async def stickymem(self, ctx, member: Member) -> None:
        await self.config.member(member).active.set(True)
        role_ids = [r.id for r in member.roles]
        role_ids.remove(member.guild.id)
        await self.config.member(member).roles.set(role_ids)
        await ctx.send(_("Stickied {member}.").format(member=member.display_name))

    @checks.admin()
    @commands.command()
    async def unstickymem(self, ctx, member: Union[Member, int]):
        if isinstance(member, Member):
            member = member.id
        await self.config.member_from_ids(ctx.guild.id, member).active.set(False)
        await ctx.send(_("{member_id} unstickied.").format(member_id=member))
