from redbot.core import commands, modlog
from datetime import timedelta
from typing import Optional
from collections import defaultdict


class ModLogStats(commands.Cog):
    def red_delete_data_for_user(self, *, requester, user_id):
        return  # This cog stores no EUD

    @commands.command()
    async def modlogstats(self, ctx, *, time: Optional[commands.TimedeltaConverter] = None):
        """Get modlog stats for the timeframe specified."""
        cases = await modlog.get_all_cases(ctx.guild, ctx.bot)
        counts = defaultdict(int)
        min_date = 0
        async with ctx.typing():
            for case in cases:
                await ctx.send("Entered for loop.")
                if case.created_at > min_date:
                    await ctx.send("Matching case")
                    counts[case.action_type] = counts[case.action_type] + 1
            await ctx.send(counts)