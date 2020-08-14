from datetime import datetime, timedelta

import discord
from discord.ext import tasks
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Bday", __file__)


@cog_i18n(_)
class Bday(commands.Cog):
    """Bday"""

    async def red_delete_data_for_user(self, *, requester, user_id):
        async with self.config.bdays() as bdays:
            for e in bdays:
                if str(e[0]) == str(user_id):
                    guild = self.bot.get_guild(int(e[1]))
                    await guild.get_user([int(e[0])]).remove_roles(
                        guild.get_role(await self.config.guild(guild).bdayRole()),
                        reason=_("User data deleted."),
                    )
                    bdays.remove(e)

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=1072001)
        default_guild = {"bdayRole": 0}
        default_global = {"bdays": []}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)
        self.bot = bot

    async def initialize(self):
        await self.bot.wait_until_red_ready()
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
                reason=_("It's their birthday!"),
            )
            await ctx.send(_("Happy birthday {} !").format(user.mention))
            async with self.config.bdays() as bdays:
                bdays.append(
                    (user.id, ctx.guild.id, (datetime.utcnow() + timedelta(days=1)).timestamp())
                )
        else:
            await ctx.send(
                _("You need to configure a birthday role first by using ``[p]setbirthday``.")
            )

    @commands.command()
    @checks.admin()
    async def setbirthday(self, ctx, role: discord.Role):
        """Set the role that will be assigned on a birthday."""
        await self.config.guild(ctx.guild).bdayRole.set(role.id)
        await ctx.send(_("The birthday role has been set to {}").format(role.name))

    @commands.command()
    @checks.mod()
    async def clearbirthdays(self, ctx):

        """Clears the birthday role off of all members."""

        for user in ctx.guild.get_role(await self.config.guild(ctx.guild).bdayRole()).members:
            await user.remove_roles(
                ctx.guild.get_role(await self.config.guild(ctx.guild).bdayRole()),
                reason=_("Birthdays cleared."),
            )

    @tasks.loop(hours=1)
    async def bdaytask(self):
        time = datetime.utcnow()
        async with self.config.bdays() as bdays:
            for bday in bdays:
                expiry = datetime.utcfromtimestamp(bday[2])
                if time > expiry:
                    guild = self.bot.get_guild(bday[1])
                    await guild.get_member(bday[0]).remove_roles(
                        guild.get_role(await self.config.guild(guild).bdayRole()),
                        reason=_("24h have passed. This birthday must be over."),
                    )
                    bdays.remove(bday)
