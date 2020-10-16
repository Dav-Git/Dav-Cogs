from redbot.core import commands, Config, checks
from discord import Member

from redbot.core.i18n import cog_i18n, Translator

from typing import Union

_ = Translator("StickyMember", __file__)


@cog_i18n(_)
class StickyMember(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, 231215102020, force_registration=True)
        default = {"roles": [], "active": False}
        self.config.register_member(**default)

    async def red_delete_data_for_user(self, *, requester, user_id):
        data = self.config.all_members()
        for g in data:
            for m in g:
                if m == user_id:
                    await self.config.member_from_ids(g, m).clear()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if await self.config.member(after).active():
            await self.config.member(after).roles.set([r.id for r in after.roles])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if await self.config.member(member).active():
            for role in await self.config.member(member).roles():
                try:
                    await member.add_roles(role)
                except Exception:  # Yes I know this is bad practice. Why is everybody analyzing my code all of a sudden? Lol
                    pass  # This currently disregards any roles that throw an exception when being assigned. I want to limit this to exceptions thrown due to role hierarchy in the future when I actually have time to figure out what error it raises.

    @checks.admin()
    @commands.command()
    async def stickymem(self, ctx, member: Member) -> None:
        await self.config.member(member).active.set(True)
        await self.config.member(member).roles.set([r.id for r in member.roles])
        await ctx.send(_("Stickied {member}.").format(member=member.display_name))

    @checks.admin()
    @commands.command()
    async def unstickymem(self, ctx, member: Union[Member, int]):
        if isinstance(member, Member):
            member = member.id
        await self.config.member_from_ids(ctx.guild.id, member).active.set(False)
        await ctx.send(_("{member_id} unstickied.").format(member_id=member))
