import logging
import discord
from redbot.core import commands, Config
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS

_ = Translator("ExclusiveRoles", __file__)


@cog_i18n(_)
class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""

    __version__ = "2.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog does not store EUD
        return

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2005200611566)
        default_guild = {"exclusives": []}
        self.config.register_guild(**default_guild)
        self.log = logging.getLogger("red.cog.dav-cogs.exclusiveroles")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            try:
                guild = before.guild
                roles = await self.config.guild(after.guild).exclusives()
                to_remove = []
                for r in roles:
                    r1, r2 = guild.get_role(r[0]), guild.get_role(r[1])
                    if None in [r1, r2]:
                        self.log.warning(
                            "Role with ID %s or %s was deleted from the guild %s (%s). Removing config entry.",
                            r[0], r[1], guild.name, guild.id,
                        )
                        to_remove.append(r)
                        continue
                    if all(role in after.roles for role in [r1, r2]):
                        try:
                            await after.remove_roles(
                                r2, reason="{} overwrites {}".format(r1.name, r2.name)
                            )
                        except discord.HTTPException as e:
                            self.log.exception(e, exc_info=True)
                if to_remove:
                    async with self.config.guild(after.guild).exclusives() as conf:
                        for r in to_remove:
                            conf.remove(r)
            except Exception as e:
                self.log.exception(e, exc_info=True)

    @commands.Cog.listener()
    async def on_guild_role_delete(self,role:discord.Role):
        async with self.config.guild(role.guild).exclusives() as conf:
            to_remove = []
            for exclusive_pair in conf:
                if role.id in exclusive_pair:
                    to_remove.append(exclusive_pair)
            for exclusive_pair in to_remove:
                conf.remove(exclusive_pair)
                self.log.warning("Removed exclusive pair with role IDs %s from guild %s (%s)",exclusive_pair, role.guild.name, role.guild.id)


    @commands.command()
    @commands.admin()
    async def exclusivenow(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. Removes the second role if both roles are present on a user."""

        await ctx.send(_("\n`Started...`\n"))
        for user in ctx.guild.members:
            if role1 in user.roles:
                if role2 in user.roles:
                    await user.remove_roles(
                        role2,
                        reason=_("Exclusivenow: {role1} overwrites {role2}").format(
                            role1=role1.name, role2=role2.name
                        ),
                    )
        await ctx.send(_("\n`Completed.`\n"))

    @commands.command()
    @commands.admin()
    async def setexclusive(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles.
        Removes the second role if the first role is assigned to a user in the future."""

        async with self.config.guild(ctx.guild).exclusives() as conf:
            conf.append((role1.id, role2.id))
        await ctx.send(_("{} will now be overwritten by {}").format(role2.name, role1.name))

    @commands.command()
    @commands.admin()
    async def unexclusive(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 roles and removes their exclusivity"""

        async with self.config.guild(ctx.guild).exclusives() as conf:
            if [role1.id, role2.id] in conf:
                try:
                    conf.remove([role1.id, role2.id])
                    await ctx.send(
                        _("{} will no longer be overwritten by {}").format(role2.name, role1.name)
                    )
                except Exception as e:
                    self.log.exception(e, exc_info=True)
                    await ctx.send(_("```An Error occured```"))
            else:
                await ctx.send(
                    _("{} and {} are not registered as exclusive roles").format(
                        role1.name, role2.name
                    )
                )

    @commands.command()
    @commands.admin()
    async def listexclusives(self, ctx):
        """List all exclusive roles"""

        roles = await self.config.guild(ctx.guild).exclusives()
        text = ""
        if roles == []:
            text = _("No exclusive roles set")
        else:
            mentions = []
            for r in roles:
                r0, r1 = ctx.guild.get_role(r[0]), ctx.guild.get_role(r[1])
                mentions.append(
                    _("\n{} overwrites {}").format(
                        r0.mention,
                        r1.mention,
                    )
                )
            text = "\n".join(mentions)
        pages = []
        for page in pagify(text, ["\n"], escape_mass_mentions=False, page_length=1000):
            embed = discord.Embed(title=_("Exclusiveroles"))
            embed.add_field(name=_("All exclusive role pairs:"), value=page)
            pages.append(embed)

        await menu(ctx, pages, DEFAULT_CONTROLS)

    @commands.command()
    @commands.admin()
    async def retroscan(self, ctx):
        """Scans the entire user list for roles that have been set as exclusive."""

        async with ctx.channel.typing():
            await ctx.send(_("``This may take a while...``"))
            roles = await self.config.guild(ctx.guild).exclusives()
            for r in roles:
                r_new = (ctx.guild.get_role(r[0]), ctx.guild.get_role(r[1]))
                if None in r_new:
                    self.log.warning(
                        "One of the roles(%s,%s) was deleted "
                        "from the guild %s (%s). Removing config entry.",
                        r[0], r[1], ctx.guild.name, ctx.guild.id,
                    )
                    roles.remove(r)
                    await self.config.guild(ctx.guild).exclusives.set(roles)
                    continue
                await ctx.send(
                    _("``Starting with {} and {}``").format(r_new[0].name, r_new[1].name)
                )
                for u in ctx.guild.members:
                    if r_new[0] in u.roles:
                        if r_new[1] in u.roles:
                            await u.remove_roles(
                                r_new[1],
                                reason=_("{} overwrites {}").format(r_new[0].name, r_new[1].name),
                            )
        await ctx.send(_("``Retroscan completed.``"))
