from redbot.core import commands, Config
from redbot.core.i18n import Translator, cog_i18n
import discord

_ = Translator("AutoRole", __file__)


@cog_i18n(_)
class AutoRoler(commands.Cog):
    """AutoRoler"""

    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        pass  # This cog stores no EUD

    def __init__(self):
        self.config = Config.get_conf(self, identifier=300920211119)
        default_guild = {
            "enabled": False,
            "roles": [],
        }
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = await self.config.guild(member.guild).all()
        if not data["enabled"]:
            return
        await member.add_roles(*[member.guild.get_role(role_id) for role_id in data["roles"]])

    @commands.group()
    async def autorole(self, ctx):
        """Autorole commands"""
        pass

    @autorole.command()
    async def add(self, ctx, role: discord.Role):
        """Add a role to be assigned to all new joins"""
        async with self.config.guild(ctx.guild).roles() as roles:
            if role.id in roles:
                await ctx.send(_("Role already in autorole list"))
                return
            roles.append(role.id)
            await ctx.send(_("{} added to autorole list").format(role.mention))

    @autorole.command()
    async def remove(self, ctx, role: discord.Role):
        """Remove a role from the autorole list"""
        async with self.config.guild(ctx.guild).roles() as roles:
            if role.id not in roles:
                await ctx.send(_("Role not in autorole list"))
                return
            roles.remove(role.id)
            await ctx.send(_("{} removed from autorole list").format(role.mention))

    @autorole.command()
    async def list(self, ctx):
        """List all roles in the autorole list"""
        async with self.config.guild(ctx.guild).roles() as roles:
            if not roles:
                await ctx.send(_("No roles in autorole list"))
                return
            role_mentions = [ctx.guild.get_role(role_id).mention for role_id in roles]
            await ctx.send(_("Autorole list: {}").format(", ".join(role_mentions)))

    @autorole.command()
    async def enable(self, ctx):
        """Enable autorole"""
        await self.config.guild(ctx.guild).enabled.set(True)
        await ctx.send(_("AutoRoler enabled"))

    @autorole.command()
    async def disable(self, ctx):
        """Disable autorole"""
        await self.config.guild(ctx.guild).enabled.set(False)
        await ctx.send(_("AutoRoler disabled"))
