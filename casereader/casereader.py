from redbot.core import modlog, commands, checks
from redbot.core.i18n import cog_i18n, Translator
import discord
from datetime import datetime

_ = Translator("CaseReader", __file__)


@cog_i18n(_)
class CaseReader(commands.Cog):
    """CaseReader"""

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog does not store EUD
        return

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def read(self, ctx, user: discord.User):
        membercases = await modlog.get_cases_for_member(ctx.guild, self.bot, member=user)
        rendered_cases = []
        for case in membercases:
            message = _("{case}\n**Timestamp**: {timestamp}").format(
                case=await case.message_content(embed=False),
                timestamp=datetime.fromtimestamp(case.created_at).strftime(
                    "%d-%b-%Y (%H:%M:%S) UTC"
                ),
            )
            rendered_cases.append(message)

        for message in rendered_cases:
            await ctx.send(
                f"--------------------------------------------------------------------\n{message}"
            )
