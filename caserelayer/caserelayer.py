from redbot.core import modlog, commands, checks
import discord
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("CaseRelayer", __file__)


@cog_i18n(_)
class CaseRelayer(commands.Cog):
    """CaseRelayer"""

    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog stores no EUD
        return

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def relay(self, ctx, case_no: int, user: discord.Member):
        try:
            case = await modlog.get_case(case_no, ctx.guild, self.bot)
        except RuntimeError:
            await ctx.send(_("That case does not exist for that server."))
            return
        embed = await case.message_content(embed=True)
        embed.remove_field(0)
        try:
            await user.send(embed=embed)
            await ctx.send(
                _("Case has been relayed to {username}#{userdiscriminator}.").format(
                    username=user.name, userdiscriminator=user.discriminator
                )
            )
        except:
            await ctx.send(_("Something went wrong."))
