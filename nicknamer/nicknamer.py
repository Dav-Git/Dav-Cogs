from redbot.core import commands, checks, modlog, Config
import discord
from typing import Optional
from datetime import datetime
from discord.ext import tasks
from redbot.core.i18n import Translator, cog_i18n
import logging

log = logging.getLogger("red.dav-cogs.nicknamer")


_ = Translator("NickNamer", __file__)


@cog_i18n(_)
class NickNamer(commands.Cog):
    """NickNamer"""

    __version__ = "2.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        if requester == "user":
            return
        elif requester == "user_strict":
            data = await self.config.all_guilds()
            for guild_id in data:
                async with self.config.guild_from_id(guild_id).active() as active:
                    for e in active:
                        if e[0] == user_id:
                            active.remove(e)
        elif requester == "owner" or requester == "discord_deleted_user":
            data = await self.config.all_guilds()
            for guild_id in data:
                async with self.config.guild_from_id(guild_id).active() as active:
                    for e in active:
                        if e[0] == user_id:
                            active.remove(e)
                async with self.config.guild_from_id(guild_id).frozen() as frozen:
                    for e in frozen:
                        if e[0] == user_id:
                            frozen.remove(e)

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=190420201535, force_registration=True)
        standard = {
            "modlog": True,
            "nick": "CHANGEME",
            "dm": False,
            "frozen": [],
            "active": [],
        }
        self.config.register_guild(**standard)
        self._rename_tempnicknames.start()

    def cog_unload(self):
        self._rename_tempnicknames.cancel()

    async def initialize(self):
        await self.register_casetypes()

    def valid_nickname(self, nickname: str):
        if len(nickname) <= 32:
            return True
        return False

    @staticmethod
    async def register_casetypes():
        forcechange_case = {
            "name": "nickchange",
            "default_setting": True,
            "image": ":pencil2:",
            "case_str": "Nickname changed",
        }
        freeze_case = {
            "name": "nickfreeze",
            "default_setting": True,
            "image": "\N{FREEZING FACE}",
            "case_str": "Nickname frozen.",
        }
        temp_case = {
            "name": "tempnick",
            "default_setting": True,
            "image": "\N{TIMER CLOCK}\N{VARIATION SELECTOR-16}",
            "case_str": "Nickname temporarily changed.",
        }
        try:
            await modlog.register_casetype(**forcechange_case)
            await modlog.register_casetype(**freeze_case)
            await modlog.register_casetype(**temp_case)
        except RuntimeError:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            settings = await self.config.guild(after.guild).frozen()
            for e in settings:
                if after.id in e:
                    if after.nick != e[1]:
                        try:
                            await after.edit(nick=e[1], reason="Nickname frozen.")
                        except discord.errors.Forbidden:
                            log.info(
                                f"Missing permissions to change {before.nick} ({before.id}) in {before.guild.id}, removing freeze"
                            )
                            async with self.config.guild(after.guild).frozen() as frozen:
                                for e in frozen:
                                    if e[0] == before.id:
                                        frozen.remove(e)

    @tasks.loop(minutes=10)
    async def _rename_tempnicknames(self):
        for guild in self.bot.guilds:
            async with self.config.guild(guild).all() as settings:
                if not settings["active"]:
                    continue
                else:
                    for e in settings["active"]:
                        expiry_time = datetime.utcfromtimestamp(e[2])
                        if datetime.utcnow() > expiry_time:
                            if guild.get_member(e[0]):
                                await guild.get_member(e[0]).edit(
                                    nick=e[1], reason=_("Temporary nickname expired.")
                                )
                            settings["active"].remove(e)
                            if settings["dm"]:
                                try:
                                    await guild.get_member(e[0]).send(
                                        _(
                                            "Your nickname in ``{guildname}`` has been reset to your original nickname."
                                        ).format(guildname=guild.name)
                                    )
                                except:
                                    pass

    @checks.mod()
    @commands.command()
    @checks.bot_has_permissions(manage_nicknames=True)
    async def nick(self, ctx, user: discord.Member, *, reason: Optional[str]):
        """Forcibly change a user's nickname to a predefined string."""
        if not reason:
            reason = _("Nickname force-changed")
        try:
            await user.edit(nick=await self.config.guild(ctx.guild).nick())
            await ctx.tick()
            if await self.config.guild(ctx.guild).modlog():
                await modlog.create_case(
                    self.bot,
                    ctx.guild,
                    datetime.now(),
                    "nickchange",
                    user,
                    moderator=ctx.author,
                    reason=reason,
                    channel=ctx.channel,
                )
            if await self.config.guild(ctx.guild).dm():
                try:
                    await user.send(
                        _(
                            "Your nickname on ``{ctxguildname}`` has been force-changed by a moderator."
                        ).format(ctxguildname=ctx.guild.name)
                    )
                except:
                    pass
        except discord.errors.Forbidden:
            await ctx.send(
                _("Missing permissions.")
            )  # can remove this as the check is made on invoke with the decorator

    @checks.mod()
    @commands.command()
    @checks.bot_has_permissions(manage_nicknames=True)
    async def cnick(self, ctx, user: discord.Member, nickname: str, *, reason: Optional[str]):
        """Forcibly change a user's nickname."""
        valid_nick_check = self.valid_nickname(nickname=nickname)
        if not valid_nick_check:
            return await ctx.send(
                "That nickname is too long. Keep it under 32 characters, please."
            )
        if not reason:
            reason = _("Nickname force-changed")
        try:
            await user.edit(nick=nickname)
            await ctx.tick()
            if await self.config.guild(ctx.guild).modlog():
                await modlog.create_case(
                    self.bot,
                    ctx.guild,
                    datetime.now(),
                    "nickchange",
                    user,
                    moderator=ctx.author,
                    reason=reason,
                    channel=ctx.channel,
                )
            if await self.config.guild(ctx.guild).dm():
                try:
                    await user.send(
                        _(
                            "Your nickname on ``{ctxguildname}`` has been force-changed by a moderator."
                        ).format(ctxguildname=ctx.guild.name)
                    )
                except:
                    pass
        except discord.errors.Forbidden:
            await ctx.send(_("Missing permissions."))

    @checks.mod()
    @commands.command()
    @checks.bot_has_permissions(manage_nicknames=True)
    async def freezenick(
        self,
        ctx,
        user: discord.Member,
        nickname: str,
        *,
        reason: Optional[str] = "Nickname frozen.",
    ):
        """Freeze a users nickname."""
        name_check = await self.config.guild(ctx.guild).frozen()
        for id in name_check:
            if user.id in id:
                return await ctx.send("User is already frozen. Unfreeze them first.")
        valid_nick_check = self.valid_nickname(nickname=nickname)
        if not valid_nick_check:
            return await ctx.send("That nickname is too long. Keep it under 32 characters, please")

        try:
            await user.edit(nick=nickname)
            await ctx.tick()
            async with self.config.guild(ctx.guild).frozen() as frozen:
                frozen.append((user.id, nickname))
            if await self.config.guild(ctx.guild).modlog():
                await modlog.create_case(
                    self.bot,
                    ctx.guild,
                    datetime.now(),
                    "nickfreeze",
                    user,
                    moderator=ctx.author,
                    reason=reason,
                    channel=ctx.channel,
                )
            if await self.config.guild(ctx.guild).dm():
                try:
                    await user.send(
                        _("Your nickname on ``{ctxguildname}`` has been frozen.").format(
                            ctxguildname=ctx.guild.name
                        )
                    )
                except:
                    pass
        except discord.errors.Forbidden:
            await ctx.send(_("Missing permissions."))

    @checks.mod()
    @commands.command()
    async def unfreezenick(self, ctx, user: discord.Member):
        """Unfreeze a user's nickname."""
        async with self.config.guild(ctx.guild).frozen() as frozen:
            for e in frozen:
                if user.id in e:
                    frozen.remove(e)
                    await ctx.tick()
                    if await self.config.guild(ctx.guild).dm():
                        try:
                            await user.send(
                                _("Your nickname on ``{ctxguildname}`` has been unfrozen.").format(
                                    ctxguildname=ctx.guild.name
                                )
                            )
                        except:
                            pass

    @checks.mod()
    @commands.command()
    @checks.bot_has_permissions(manage_nicknames=True)
    async def tempnick(
        self,
        ctx,
        user: discord.Member,
        duration: commands.TimedeltaConverter,
        nickname: str,
        *,
        reason: Optional[str] = "User has been temporarily renamed.",
    ):
        """Temporarily rename a user.\n**IMPORTANT**: For better performance, temporary nicknames are checked in a 10 minute intervall."""
        valid_nick_check = self.valid_nickname(nickname=nickname)
        if not valid_nick_check:
            return await ctx.send(
                "That nickname is too long. Keep it under 32 characters, please."
            )
        try:
            oldnick = user.nick
            await user.edit(nick=nickname)
            await ctx.tick()
            change_end = datetime.utcnow() + duration
            async with self.config.guild(ctx.guild).active() as active:
                active.append((user.id, oldnick, change_end.timestamp()))
            if self.config.guild(ctx.guild).modlog():
                await modlog.create_case(
                    self.bot,
                    ctx.guild,
                    datetime.now(),
                    "tempnick",
                    user,
                    moderator=ctx.author,
                    reason=reason,
                    channel=ctx.channel,
                )
            if await self.config.guild(ctx.guild).dm():
                try:
                    await user.send(
                        _(
                            "Your nickname in ``{ctxguildname}`` has been temporarily changed."
                        ).format(ctxguildname=ctx.guild.name)
                    )
                except:
                    pass
        except discord.errors.Forbidden:
            await ctx.send(_("Missing permissions."))

    @checks.admin()
    @commands.group()
    @checks.bot_has_permissions(manage_nicknames=True)
    async def nickset(self, ctx):
        """Nicknamer settings"""
        pass

    @nickset.command()
    async def name(self, ctx, *, name: str):
        """Set the default name that will be applied when using ``[p]nick``"""
        if len(name) < 33 and len(name) > 1:
            await self.config.guild(ctx.guild).nick.set(name)
            await ctx.send(_("Standard Nickname set to ``{name}``.").format(name=name))

    @nickset.command()
    async def modlog(self, ctx, true_or_false: bool):
        """Set if you would like to create a modlog entry everytime a nickname is being changed."""
        await self.config.guild(ctx.guild).modlog.set(true_or_false)
        await ctx.send(
            _("Modlog entries set to {true_or_false}.").format(true_or_false=true_or_false)
        )

    @nickset.command()
    async def dm(self, ctx, true_or_false: bool):
        """Set if you would like the bot to DM the user who's nickname was changed."""
        await self.config.guild(ctx.guild).dm.set(true_or_false)
        await ctx.send(
            _("Sending a DM set to {true_or_false}.").format(true_or_false=true_or_false)
        )

    @checks.admin()
    @commands.command()
    async def nickpurge(self, ctx, are_you_sure: Optional[bool]):
        """Remove all nicknames in the server."""
        if are_you_sure:
            for member in ctx.guild.members:
                if member.nick:
                    await member.edit(nick=None, reason="Nickname purge")
            await ctx.send(_("Nicknames purged"))
        else:
            await ctx.send(
                _(
                    "This will remove the nicknames of all members. If you are sure you want to do this run:\n{command}"
                ).format(command=f"``{ctx.clean_prefix}nickpurge yes``")
            )
