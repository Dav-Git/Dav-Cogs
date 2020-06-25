from redbot.core import commands, checks
import discord
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Check", __file__)


@cog_i18n(_)
class Check(commands.Cog):
    """Check"""

    def __init__(self):
        pass

    @commands.command()
    @checks.mod()
    async def check(self, ctx, user: discord.User):
        ctx.assume_yes = True
        member = False
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
                ).format(userid=user.id)
            )
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
