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
            await ctx.invoke(ctx.bot.get_command("userinfo"), user=user)
        except:
            pass
        try:
            await ctx.invoke(ctx.bot.get_command("read"), user=user)
        except:
            await ctx.invoke(ctx.bot.get_command("warnings"), user=user)
        try:
            await ctx.invoke(ctx.bot.get_command("listflag"), member=user)
        except:
            pass
