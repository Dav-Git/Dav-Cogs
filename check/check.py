from redbot.core import commands, checks
import discord
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Check", __file__)


@cog_i18n(_)
class Check(commands.Cog):
    """Check"""

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @checks.mod()
    async def check(self, ctx, userid: int):
        user = None
        try:
            user = self.bot.fetch_user(userid)
        except:
            await ctx.send(_("User {userid} not found.").format(userid=userid))
        ctx.assume_yes = True
        member = False
        if user is None:
            user = self.bot.get_user(userid)
        try:
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
                ).format(userid=userid)
            )
        except InboundLocalError:
            return
        try:
            if member:
                await ctx.invoke(ctx.bot.get_command("userinfo"), user=member)
        except:
            pass
        try:
            await ctx.invoke(ctx.bot.get_command("read"), user=user)
        except:
            if member:
                await ctx.invoke(ctx.bot.get_command("warnings"), user=member)
        try:
            await ctx.invoke(ctx.bot.get_command("listflag"), member=user)
        except:
            pass

        await ctx.send(_("Lookup completed."))
