from redbot.core import commands, Config
from redbot.core.i18n import cog_i18n, Translator
from asyncio import sleep
import discord

_ = Translator("JoinFlag", __file__)


@cog_i18n(_)
class JoinFlag(commands.Cog):
    """JoinFlag"""

    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog stores moderation data so we won't delete it.
        return

    def __init__(self):
        self.config = Config.get_conf(self, 12345, force_registration=True)
        self.config.register_member(flag=None)
        self.config.register_guild(channel=None)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not await self.check_config(member.guild):
            return
        if await self.config.member(member).flag():
            await sleep(1)
            await member.guild.get_channel(await self.config.guild(member.guild).channel()).send(
                _("**This member ({m}) was flagged after leaving!**\n{flag}").format(
                    m=member.display_name, flag=await self.config.member(member).flag()
                )
            )
            await self.config.member(member).flag.set(None)

    @commands.command()
    @commands.mod()
    async def joinflag(self, ctx, user_id: int, *, text: str):
        """Put a note on a user. It will be displayed when they re-join the server."""
        if not await self.check_config(ctx.guild):
            return await ctx.send(_("You need to set a display-channel first."))
        await self.config.member_from_ids(ctx.guild.id, user_id).flag.set(text)
        await ctx.tick()

    @commands.group()
    @commands.admin()
    async def joinflagset(self, ctx):
        """JoinFlag settings"""
        pass

    @joinflagset.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the channel where the flag will be displayed."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.tick()

    async def check_config(self, guild):
        if not await self.config.guild(guild).channel():
            return False
        return True
