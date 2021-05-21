from datetime import datetime, timedelta
from typing import Optional
import discord
from discord.ext import tasks
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Bday", __file__)


@cog_i18n(_)
class Bday(commands.Cog):
    """Bday"""

    __version__ = "0.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        await self.config.user_from_id(user_id).clear()

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=1072001)
        default_guild = {"bdayRole": 0}
        default_user = {"bday": None}
        self.config.register_guild(**default_guild)
        self.config.register_user(**default_user)
        self.bot = bot
        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_red_ready()
        self.bdaytask.start()

    def cog_unload(self):
        self.bdaytask.cancel()

    @tasks.loop(hours=1)
    async def bdaytask(self):
        await self.bot.wait_until_red_ready()
        date = datetime.utcnow().strftime("%d%m")
        for user_id in await self.config.all_users():
            if date == await self.config.user_from_id(user_id).bday():
                for guild_id in await self.config.all_guilds():
                    member = self.bot.get_guild(guild_id).get_member(user_id)
                    if member and not await self.bot.cog_disabled_in_guild_raw("Bday", guild_id):
                        await member.add_roles(
                            member.guild.get_roles(
                                await self.config.guild_from_id(guild_id).bdayRole()
                            )
                        )
            else:
                for guild_id in await self.config.all_guilds():
                    member = self.bot.get_guild(guild_id).get_member(user_id)
                    if (
                        member
                        and (not await self.bot.cog_disabled_in_guild_raw("Bday", guild_id))
                        and (
                            (
                                role := member.guild.get_roles(
                                    await self.config.guild_from_id(guild_id).bdayRole()
                                )
                            )
                            in member.roles
                        )
                    ):
                        await member.remove_roles(role)

    @commands.command()
    @checks.mod()
    async def birthday(self, ctx, date: Optional[str] = None):
        """Set your birthday.\nOmit a date to set your birthday as today.\nDate format: 'ddMM'"""
        if date is None:
            date = datetime.utcnow().strftime("%d%m")
        await self.config.user_from_id(ctx.author.id).bday.set(date)
        await ctx.tick()

    @commands.command()
    @checks.admin()
    async def setbirthdayrole(self, ctx, role: discord.Role):
        """Set the role that will be assigned on a birthday."""
        await self.config.guild(ctx.guild).bdayRole.set(role.id)
        await ctx.send(_("The birthday role has been set to {}").format(role.name))
