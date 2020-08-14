import discord
from redbot.core import commands, checks
from typing import Optional


class Mover(commands.Cog):
    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog does not store EUD
        return

    @commands.command()
    @checks.mod()
    async def massmove(
        self, ctx, target: discord.VoiceChannel, source: Optional[discord.VoiceChannel]
    ):
        if not source:
            source = ctx.author.voice.channel

        for u in source.members:
            await u.move_to(target, reason="Massmove")
