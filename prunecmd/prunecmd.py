from typing import Optional

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Prunecmd", __file__)


@cog_i18n(_)
class Prunecmd(commands.Cog):
    """Prunecmd"""

    __version__ = "2.0.1"

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
    @commands.admin()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    async def prunecmd(self, ctx, days: Optional[int] = 1, confirm: Optional[bool] = False):
        """Prunes the discord member list of your guild. This will kick all users without a role and x days inactivity."""
        if days > 30 or days < 1:
            await ctx.send(_("The days parameter must be between 1 and 30."))
            return
        if ctx.assume_yes or confirm:
            x = await ctx.guild.prune_members(
                days=days, compute_prune_count=True, reason="Member prune"
            )
            await ctx.send(
                _("The member list has been pruned successfully. {x} members were kicked.").format(
                    x=x
                )
            )
        else:
            x = await ctx.guild.estimate_pruned_members(days=days)
            await ctx.send(
                _(
                    "This will kick {x} members from your guild. If you are sure you want to proceed run {command}"
                ).format(command=f"``{ctx.clean_prefix}prunecmd {days} yes``", x=x)
            )
