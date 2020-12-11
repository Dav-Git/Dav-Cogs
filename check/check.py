from redbot.core import commands, checks
import discord
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Check", __file__)


@cog_i18n(_)
class Check(commands.Cog):
    """Check"""

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog stores no EUD
        return

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.mod()
    async def check(self, ctx, member: discord.Member):
        ctx.assume_yes = True
        async with ctx.typing():
            await ctx.send(
                _(":mag_right: Starting lookup for: {usermention}({userid})").format(
                    usermention=member.mention, userid=member.id
                )
            )
            await self._userinfo(ctx, member)
            await self._warnings_or_read(ctx, member)
            await self._maybe_listflag(ctx, member)

        await ctx.send(_("Lookup completed."))

    async def _userinfo(self, ctx, member):
        try:
            await ctx.invoke(ctx.bot.get_command("userinfo"), user=member)
        except:
            pass

    async def _warnings_or_read(self, ctx, member):
        user = ctx.bot.get_user(member.id)
        try:
            await ctx.invoke(ctx.bot.get_command("read"), user=user)
        except:
            try:
                await ctx.invoke(ctx.bot.get_command("warnings"), user=member)
            except:
                pass

    async def _maybe_listflag(self, ctx, member):
        try:
            await ctx.invoke(ctx.bot.get_command("listflag"), member=member)
        except:
            pass
