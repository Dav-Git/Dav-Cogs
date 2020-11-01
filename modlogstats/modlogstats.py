from redbot.core import commands, modlog
from datetime import timedelta
from typing import Optional


class ModLogStats(commands.Cog):
    def red_delete_data_for_user(self, *, requester, user_id):
        return  # This cog stores no EUD

    @commands.command()
    async def modlogstats(self, ctx, *, time: Optional[commands.TimedeltaConverter] = None):
        """Get modlog stats for the timeframe specified."""
        cases = modlog.get_all_cases(ctx.guild, ctx.bot)
        types = []
