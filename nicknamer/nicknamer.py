from redbot.core import commands, checks, modlog, Config
import discord
from typing import Optional
from datetime import datetime
from discord.ext import tasks
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("NickNamer", __file__)


@cog_i18n(_)
class NickNamer(commands.Cog):
    """NickNamer"""

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
                        await after.edit(nick=e[1], reason="Nickname frozen.")

    @tasks.loop(minutes=10)
    async def _rename_tempnicknames(self):
        for guild in self.bot.guilds:
            async with await self.config.guild(guild).all() as settings:
                if not settings["active"]:
                    continue
                else:
                    for e in settings["active"]:
                        expiry_time = datetime.utcfromtimestamp(e[2])
                        if datetime.utcnow() > expiry_time:
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
    async def nick(self, ctx, user: discord.Member, *, reason: Optional[str]):
        """Forcibly change a user's nickname to a predefined string."""
        if not reason:
            reason = _("Nickname force-changed")
        try:
            await user.edit(nick=await self.config.guild(ctx.guild).nick())
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
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
    async def cnick(self, ctx, user: discord.Member, nickname: str, *, reason: Optional[str]):
        """Forcibly change a user's nickname."""
        if not reason:
            reason = _("Nickname force-changed")
        try:
            await user.edit(nick=nickname)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
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
    async def freezenick(
        self,
        ctx,
        user: discord.Member,
        nickname: str,
        *,
        reason: Optional[str] = "Nickname frozen.",
    ):
        """Freeze a users nickname."""
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

