import logging

import discord
from redbot.core import checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Check", __file__)


@cog_i18n(_)
class Check(commands.Cog):
    """Check"""

    __version__ = "2.1.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog stores no EUD
        return

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("red.cog.dav-cogs.check")

    @commands.command()
    @checks.mod()
    @commands.max_concurrency(1, commands.BucketType.guild)
    async def check(self, ctx, member: discord.Member):
        ctx.assume_yes = True
        async with ctx.typing():
            await ctx.send(
                _(":mag_right: Starting lookup for: {usermention}({userid})").format(
                    usermention=member.mention, userid=member.id
                )
            )
            await self._userinfo(ctx, member)
            await self._maybe_altmarker(ctx, member)
            await self._warnings_or_read(ctx, member)
            await self._maybe_listflag(ctx, member)

        await ctx.send(_("Lookup completed."))

    async def _userinfo(self, ctx, member):
        try:
            await ctx.invoke(ctx.bot.get_command("userinfo"), member=member)
        except TypeError:
            try:
                await ctx.invoke(ctx.bot.get_command("userinfo"), user=member)
            except:
                pass
        except Exception as e:
            self.log.exception(f"Error in userinfo {e}", exc_info=True)

    async def _warnings_or_read(self, ctx, member):
        try:
            await ctx.invoke(ctx.bot.get_command("read"), member=member.id)
        except:
            try:
                await ctx.invoke(ctx.bot.get_command("warnings"), member=member.id)
            except:
                self.log.debug("Command warn not found.")

    async def _maybe_listflag(self, ctx, member):
        try:
            await ctx.invoke(ctx.bot.get_command("listflag"), member=member)
        except:
            self.log.debug("Command listflag not found.")

    async def _maybe_altmarker(self, ctx, member):
        try:
            await ctx.invoke(ctx.bot.get_command("alt get"), member=member)
        except:
            self.log.debug("Altmarker not found.")
