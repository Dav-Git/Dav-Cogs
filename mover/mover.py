import discord
from redbot.core import commands
from typing import Optional


class Mover(commands.Cog):
    __version__ = "2.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog does not store EUD
        return

    @commands.command()
    @commands.mod()
    @commands.bot_has_permissions(move_members=True)
    async def massmove(
        self, ctx, target: discord.VoiceChannel, source: Optional[discord.VoiceChannel]
    ):
        if not source:
            source = ctx.author.voice.channel

        for u in source.members:
            await u.move_to(target, reason=f"Massmoved by {ctx.author}")
