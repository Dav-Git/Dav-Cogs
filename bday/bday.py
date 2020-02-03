import discord
from discord.ext import tasks
from redbot.core import commands, checks, Config


class Bday(commands.Cog):
    """Bday"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=1072001)
        default_guild = {"bdayRole": 0}
        self.config.register_guild(**default_guild)

    @commands.command()
    @checks.mod()
    async def birthday(self, ctx, user: discord.Member):

        """Assigns the birthday role to a member and sends birthday wishes."""

        if not await self.config.guild(ctx.guild).bdayRole() == 0:
            await user.add_roles(
                ctx.guild.get_role(await self.config.guild(ctx.guild).bdayRole()),
                reason="It's their birthday!",
            )
            await ctx.send("Happy birthday {} !".format(user.mention))
        else:
            await ctx.send(
                "You need to configure a birthday role first by using ``[p]setbirthday``."
            )

    @commands.command()
    @checks.admin()
    async def setbirthday(self, ctx, role: discord.Role):

        """Set the role that will be assigned on a birthday."""

        await self.config.guild(ctx.guild).bdayRole.set(role.id)
        await ctx.send("The birthday role has been set to {}".format(role.name))

    @commands.command()
    @checks.mod()
    async def clearbirthdays(self, ctx):

        """Clears the birthday role off of all members."""

        for user in ctx.guild.get_role(await self.config.guild(ctx.guild).bdayRole()).members:
            await user.remove_roles(
                ctx.guild.get_role(await self.config.guild(ctx.guild).bdayRole()),
                reason="It's a new day. The birthdays are over.",
            )

