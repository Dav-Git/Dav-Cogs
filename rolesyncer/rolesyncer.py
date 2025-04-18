import logging
import discord
from redbot.core import commands, Config
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import pagify

_ = Translator("RoleSyncer", __file__)


@cog_i18n(_)
class RoleSyncer(commands.Cog):
    """Sync Roles"""

    __version__ = "2.0.3"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester, user_id):
        # This cog doesn't store EUD
        return

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=235228062020)
        default_guild = {"onesync": [], "twosync": []}
        self.config.register_guild(**default_guild)
        self.log = logging.getLogger("red.cog.dav-cogs.rolesyncer")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            guild = before.guild
            roles = await self.config.guild(after.guild).all()
            for r in roles["onesync"]:
                r1, r2 = guild.get_role(r[0]), guild.get_role(r[1])
                if r1 in after.roles:
                    try:
                        await after.add_roles(
                            r2,
                            reason=_("One-way rolesync / {r1name} added.").format(r1name=r1.name),
                        )
                    except discord.Forbidden as f_to_pay_respect:
                        self.log.warning(
                            "Couldn't assign %s to %s. Missing permissions.\n%s",
                            r2.name,
                            after.name,
                            f_to_pay_respect,
                        )
                    except discord.HTTPException as exception:
                        self.log.exception(exception, exc_info=True)
                elif r1 in before.roles:
                    try:
                        await after.remove_roles(
                            r2,
                            reason=_("One-way rolesync / {r1name} removed.").format(
                                r1name=r1.name
                            ),
                        )
                    except discord.HTTPException as exception:
                        self.log.exception(exception, exc_info=True)
            for r in roles["twosync"]:
                r1, r2 = guild.get_role(r[0]), guild.get_role(r[1])
                if r1 in before.roles and r2 in before.roles:
                    if not r1 in after.roles:
                        try:
                            await after.remove_roles(
                                r2,
                                reason=_("Two-way rolesync / {r1name} removed.").format(
                                    r1name=r1.name
                                ),
                            )
                        except discord.HTTPException as exception:
                            self.log.exception(exception, exc_info=True)
                    elif not r2 in after.roles:
                        try:
                            await after.remove_roles(
                                r1,
                                reason=_("Two-way rolesync / {r2name} removed.").format(
                                    r2name=r2.name
                                ),
                            )
                        except discord.HTTPException as exception:
                            self.log.exception(exception, exc_info=True)
                elif r1 in after.roles:
                    try:
                        await after.add_roles(r2, reason=_("Two-way rolesync"))
                    except discord.HTTPException as exception:
                        self.log.exception(exception, exc_info=True)
                elif r2 in after.roles:
                    try:
                        await after.add_roles(r1, reason=_("Two-way rolesync"))
                    except discord.HTTPException as exception:
                        self.log.exception(exception, exc_info=True)

    @commands.bot_has_permissions(manage_roles=True)
    @commands.group(name="sync")
    async def rolesyncer(self, ctx):
        """Sync roles"""
        pass

    @rolesyncer.command()
    @commands.admin()
    async def oneway(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. If the first role is assigned to a user, the second one will be assigned as well."""

        async with self.config.guild(ctx.guild).onesync() as conf:
            conf.append((role1.id, role2.id))
        await ctx.send(
            _("{role2name} will now be synced to {role1name}").format(
                role2name=role2.name, role1name=role1.name
            )
        )

    @rolesyncer.command()
    @commands.admin()
    async def twoway(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. If either role is assigned to a user, the other one will be assigned as well."""

        async with self.config.guild(ctx.guild).twosync() as conf:
            conf.append((role1.id, role2.id))
        await ctx.send(
            _("{role1name} and {role2name} will now be synced.").format(
                role1name=role1.name, role2name=role2.name
            )
        )

    @commands.group()
    @commands.admin()
    async def unsync(self, ctx):
        """Unsync roles"""
        pass

    @unsync.command(name="oneway")
    @commands.admin()
    async def unsync_oneway(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 roles and removes their sync"""
        if await self.remove_owsync(ctx.guild, role1, role2):
            await ctx.send(
                _("Sync removed from {role1name} and {role2name}.").format(
                    role1name=role1.name, role2name=role2.name
                )
            )
        else:
            await ctx.send(_("Couldn't find these roles in the sync database."))

    @unsync.command(name="twoway")
    @commands.admin()
    async def unsync_twoway(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 roles and removes their sync"""
        if await self.remove_twsync(ctx.guild, role1, role2):
            await ctx.send(
                _("Sync removed from {role1name} and {role2name}.").format(
                    role1name=role1.name, role2name=role2.name
                )
            )
        else:
            await ctx.send(_("Couldn't find these roles in the sync database."))

    @commands.command()
    @commands.admin()
    async def listsync(self, ctx):
        """List all exclusive roles"""

        settings = await self.config.guild(ctx.guild).all()
        embed = discord.Embed(title=_("Rolesync"))
        mentions = []
        for roles in settings["onesync"]:
            role1 = ctx.guild.get_role(roles[0])
            if (role2 := ctx.guild.get_role(roles[1])) and role1:
                mentions.append(f"{role1.mention} --> {role2.mention}")
            else:
                await self.remove_owsync(ctx.guild, role1, role2)
        text = "\n".join(mentions)
        if not text:
            text = _("No roles in one-way sync.")
        if len(text) > 1024:
            for page in pagify(_("One-way sync:\n{text}").format(text=text), shorten_by=15):
                await ctx.send(page)
        else:
            embed.add_field(name=_("One-way sync:"), value=text)
        mentions = []
        for roles in settings["twosync"]:
            role1 = ctx.guild.get_role(roles[0])
            if (role2 := ctx.guild.get_role(roles[1])) and role1:
                mentions.append(f"{role1.mention} <-> {role2.mention}")
            else:
                await self.remove_twsync(ctx.guild, role1, role2)
        text2 = "\n".join(mentions)
        if not text2:
            text2 = _("No roles in two-way sync.")
        if len(text2) > 1024:
            for page in pagify(_("Two-way sync:\n{text}").format(text=text2), shorten_by=15):
                await ctx.send(page)
        else:
            embed.add_field(name=_("Two-way sync:"), value=text2)
        if embed.fields:
            await ctx.send(embed=embed)

    async def remove_owsync(
        self, guild: discord.Guild, role1: discord.Role, role2: discord.Role
    ) -> bool:
        """Remove one way sync from config"""
        async with self.config.guild(guild).onesync() as conf:
            for e in conf:
                if role1.id in e and role2.id in e:
                    conf.remove(e)
                    return True
        return False

    async def remove_twsync(
        self, guild: discord.Guild, role1: discord.Role, role2: discord.Role
    ) -> bool:
        """Remove two way sync from config"""
        async with self.config.guild(guild).twosync() as conf:
            for e in conf:
                if role1.id in e and role2.id in e:
                    conf.remove(e)
                    return True
        return False
