from dataclasses import dataclass
from typing import List

import discord
from redbot.core import Config, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import box

from .exceptions import AltAlreadyRegistered, AltNotRegistered

_ = Translator("AltMarker", __file__)


@dataclass
class Alt:
    id: int
    name: str

    @classmethod
    def from_dict(cls, data):
        a = cls(None, None)
        a.__dict__.update(data)
        return a


@cog_i18n(_)
class AltMarker(commands.Cog):
    """
    Mark alt accounts
    """

    __version__ = "0.1.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, user_id, requester):
        pass  # TODO

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=232329032022)
        self.config.register_member(alts=[])

    @commands.group()
    async def alt(self, ctx: commands.Context):
        """Mark or unmark an alt acount"""

    @alt.command(aliases=["add"])
    async def mark(self, ctx: commands.Context, user: discord.Member, alt: discord.Member):
        """Mark an alt account"""
        try:
            await self.add_alt(user, alt)
            await ctx.send(
                _("{alt} is now marked as an alt of {user}.").format(alt=alt, user=user)
            )
        except AltAlreadyRegistered as error:
            await ctx.send(error.message)
        finally:
            await ctx.send(await self._get_alts_string(user))

    @commands.mod()
    @alt.command()
    async def get(self, ctx: commands.Context, user: discord.Member):
        """Get alts of a member"""
        await ctx.send(await self._get_alts_string(user))

    @alt.command(aliases=["remove", "delete"])
    async def unmark(self, ctx: commands.Context, user: discord.Member, alt: discord.Member):
        """Unmark an alt account"""
        try:
            await self.remove_alt(user, alt)
            await ctx.send(
                _("{alt} is no longer marked as an alt of {user}.").format(alt=alt, user=user)
            )
        except AltNotRegistered as error:
            await ctx.send(error.message)
        finally:
            await ctx.send(await self._get_alts_string(user))

    @commands.group()
    async def amset(self, ctx: commands.Context):
        """Set altmarker settings"""

    async def add_alt(self, member: discord.Member, alt: discord.Member) -> None:
        """Add an alt to a member"""
        if not await self.is_alt(member, alt):
            alts = await self.get_alts(member) + await self.get_alts(alt)
            alts.append(Alt(alt.id, str(alt)))
            alts.append(Alt(member.id, str(member)))
            await self._save_alt_list(member.guild, alts)
        else:
            raise AltAlreadyRegistered(
                _("{alt} is already an alt of {member}.").format(alt=alt, member=member),
                member=member,
                alt=alt,
            )

    async def remove_alt(self, member: discord.Member, alt: discord.Member) -> None:
        """Remove an alt from a member"""
        if await self.is_alt(member, alt):
            alts = await self.get_alts(member)
            await self.config.member(alt).clear()
            alts = [a for a in alts if a.id != alt.id]  # Delete alt from list
            alts.append(
                Alt(member.id, str(member))
            )  # Make sure config entry for member gets updated
            await self._save_alt_list(member.guild, alts)
        else:
            raise AltNotRegistered(
                _("{alt} is not an alt of {member}.").format(alt=alt, member=member),
                member=member,
                alt=alt,
            )

    async def get_alts(self, member: discord.Member) -> List[Alt]:
        """Get alts of a member"""
        return [Alt.from_dict(a) for a in await self.config.member(member).alts()]

    async def is_alt(self, member: discord.Member, alt: discord.Member) -> bool:
        alts = await self.get_alts(member)
        for a in alts:
            if a.id == alt.id:
                return True
        return False

    async def _get_alts_string(self, member: discord.Member) -> str:
        return _("Known accounts of {member}: {alts}").format(
            member=member,
            alts=box(
                "\n - " + "\n - ".join([f"{a.name}({a.id})" for a in await self.get_alts(member)]),
                lang="md",
            ),
        )

    async def _save_alt_list(self, guild: discord.Guild, alts: List[Alt]):
        for alt_account in alts:
            altcopy = alts.copy()
            altcopy.remove(alt_account)
            altcopy = [a.__dict__ for a in altcopy]
            await self.config.member_from_ids(guild.id, alt_account.id).alts.set(altcopy)