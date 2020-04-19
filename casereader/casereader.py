from redbot.core import modlog, commands, checks
import discord


class CaseReader(commands.Cog):
    """CaseReader"""

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def read(self, ctx, user: discord.User):
        membercases = await modlog.get_cases_for_member(ctx.guild, self.bot, member=user)
        embed_requested = await ctx.embed_requested()
        rendered_cases = [
            await case.message_content(embed=embed_requested) for case in membercases
        ]
        for message in rendered_cases:
            await ctx.send(embed=message)
