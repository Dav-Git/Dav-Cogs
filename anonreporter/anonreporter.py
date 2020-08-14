from redbot.core import commands, checks, Config
from redbot.core.i18n import cog_i18n, Translator

import discord

_ = Translator("AnonReporter", __file__)


@cog_i18n(_)
class AnonReporter(commands.Cog):
    async def red_delete_data_for_user(self, *, user_id, requester):
        return  # This cog stores no EUD

    def __init__(self):
        self.config = Config.get_conf(self, identifier=171814082020, force_registration=True)
        default_guild = {"channel": None}
        default_global = {"rep_guild": None, "rep_channel": None}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

    @checks.admin()
    @commands.group()
    async def anonreporter(self, ctx):
        """Anonreporter settings"""
        pass

    @commands.guild_only()
    @anonreporter.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the channel used for guild reports."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.send(_("Report channel set to {channel}").format(channel=channel.mention))

    @commands.guild_only()
    @checks.is_owner()
    @anonreporter.command(name="global")
    async def global_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for global reports."""
        await self.config.rep_guild.set(ctx.guild.id)
        await self.config.rep_channel.set(channel.id)
        await ctx.send(
            _("Global reports channel set to {channel} in {guild}").format(
                channel=channel.mention, guild=ctx.guild.name
            )
        )
