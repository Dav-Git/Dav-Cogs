from redbot.core import commands, checks
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Prunecmd", __file__)


@cog_i18n(_)
class Prunecmd(commands.Cog):
    """Prunecmd"""

    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog stores no EUD
        return

    def __init__(self):
        pass

    @commands.command()
    @checks.admin()
    async def prunecmd(self, ctx, confirm: bool):

        """Prunes the discord member list of your guild. This will kick all users without a role and 24h inactivity."""
        if ctx.assume_yes or confirm:
            await ctx.guild.prune_members(days=1, compute_prune_count=False, reason="Member prune")
            await ctx.send(_("The member list has been pruned successfully"))
        else:
            await ctx.send(
                _(
                    "This will kick members from your guild. If you are sure you want to proceed run {command}"
                ).format(command=f"``{ctx.clean_prefix}prunecmd yes``")
            )
