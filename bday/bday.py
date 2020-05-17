import discord
from datetime import datetime
from discord.ext import tasks
from redbot.core import commands, checks, Config


class Bday(commands.Cog):
    """Bday"""

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=1072001)
        default_guild = {"bdayRole": 0}
        default_global = {"bdays": []}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)
        self.bot = bot
        self.bdaytask.start()

    def cog_unload(self):
        self.bdaytask.cancel()

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
            async with self.config.bdays() as bdays:
                bdays.append((user.id, ctx.guild.id, datetime.utcnow()))
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
                reason="Birthdays cleared.",
            )

    @tasks.loop(hours=1)
    async def bdaytask(self):
        time = datetime.utcnow()
        async with self.config.bdays() as bdays:
            for bday in bdays:
                delta = bday[2] - time
                if delta.seconds > 86400:
                    guild = self.bot.get_guild(bday[1])
                    await guild.get_member(bday[0]).remove_roles(
                        guild.get_role(await self.config.guild(guild).bdayRole()),
                        reason="24h have passed. This birthday must be over.",
                    )
