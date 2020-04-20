from redbot.core import commands, checks
import discord


class Check(commands.Cog):
    """Check"""

    def __init__(self):
        pass

    @commands.command()
    @checks.mod()
    async def check(self, ctx, user: discord.User):
        ctx.assume_yes = True
        try:
            member = ctx.guild.get_member(user.id)
            await ctx.send(f":mag_right: Starting lookup for: {user.mention}({user.id})")
        except AttributeError:
            await ctx.send(
                f":mag: This user is not in your guild anymore. Fetching reduced information for UID: {user.id}."
            )
        try:
            await ctx.invoke(ctx.bot.get_command("userinfo"), user=member)
        except:
            pass
        try:
            await ctx.invoke(ctx.bot.get_command("read"), user=user)
        except:
            await ctx.invoke(ctx.bot.get_command("warnings"), user=member)
        try:
            await ctx.invoke(ctx.bot.get_command("listflag"), member=user)
        except:
            pass
