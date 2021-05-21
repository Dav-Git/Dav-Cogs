from redbot.core import modlog, commands, checks
from redbot.core.i18n import cog_i18n, Translator
import discord
from datetime import datetime
from typing import Union

_ = Translator("CaseReader", __file__)


@cog_i18n(_)
class CaseReader(commands.Cog):
    """CaseReader"""

    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog does not store EUD
        return

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def read(self, ctx, member: Union[discord.User, int]):
        try:
            if isinstance(member, int):
                membercases = await modlog.get_cases_for_member(
                    bot=ctx.bot, guild=ctx.guild, member_id=member
                )
            else:
                membercases = await modlog.get_cases_for_member(
                    bot=ctx.bot, guild=ctx.guild, member=member
                )
        except discord.NotFound:
            return await ctx.send(_("This user does not exist."))
        except discord.HTTPException:
            return await ctx.send(
                _("Something unexpected went wrong while fetching that user by ID.")
            )
        if not membercases:
            return await ctx.send(_("This user has no cases."))
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
