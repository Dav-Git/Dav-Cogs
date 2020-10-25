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
    async def check(self, ctx, user: discord.User):
        ctx.assume_yes = True
        member = False
        try:
            async with ctx.typing():
                member = ctx.guild.get_member(user.id)
                await ctx.send(
                    _(":mag_right: Starting lookup for: {usermention}({userid})").format(
                        usermention=user.mention, userid=user.id
                    )
                )
        except AttributeError:
            await ctx.send(
                _(
                    ":mag: This user is not in your guild anymore. Fetching reduced information for UID: {userid}."
                ).format(userid=user.id)
            )
        try:
            async with ctx.typing():
                if member:
                    await ctx.invoke(ctx.bot.get_command("userinfo"), user=member)
        except:
            pass
        try:
            async with ctx.typing():
                await ctx.invoke(ctx.bot.get_command("read"), user=user)
        except:
            try:
                async with ctx.typing():
                    if member:
                        await ctx.invoke(ctx.bot.get_command("warnings"), user=member)
            except:
                pass
        try:
            async with ctx.typing():
                await ctx.invoke(ctx.bot.get_command("listflag"), member=member)
        except:
            pass

        await ctx.send(_("Lookup completed."))
