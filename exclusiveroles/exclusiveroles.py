import logging
import discord
from redbot.core import commands, checks, Config
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("ExclusiveRoles", __file__)


@cog_i18n(_)
class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""

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
                for r in roles:
                    r1, r2 = guild.get_role(r[0]), guild.get_role(r[1])
                    if all(role in after.roles for role in [r1, r2]):
                        try:
                            await after.remove_roles(
                                r2, reason="{} overwrites {}".format(r1.name, r2.name)
                            )
                        except discord.HTTPException as e:
                            self.log.exception(e, exc_info=True)
            except Exception as e:
                self.log.exception(e, exc_info=True)

    @commands.command()
    @checks.admin()
    async def exclusivenow(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. Removes the second role if both roles are present on a user. """

        if not isinstance(role1, discord.Role) or not isinstance(role2, discord.Role):
            return await ctx.send(_("You need to provide at least 2 roles"))

        else:
            await ctx.send(_("\n`Started...`\n"))
            for user in ctx.guild.members:
                if role1 in user.roles:
                    if role2 in user.roles:
                        await user.remove_roles(role2)
            await ctx.send(_("\n`Completed.`\n"))

    @commands.command()
    @checks.admin()
    async def setexclusive(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 Roles. Removes the second role if the first role is assigned to a user in the future. """

        async with self.config.guild(ctx.guild).exclusives() as conf:
            conf.append((role1.id, role2.id))
        await ctx.send(_("{} will now be overwritten by {}").format(role2.name, role1.name))

    @commands.command()
    @checks.admin()
    async def unexclusive(self, ctx, role1: discord.Role, role2: discord.Role):
        """Takes 2 roles and removes their exclusivity"""

        async with self.config.guild(ctx.guild).exclusives() as conf:
            if (role1.id, role2.id) in conf:
                try:
                    conf.remove((role1.id, role2.id))
                    await ctx.send(
                        _("{} will no longer be overwritten by {}").format(role2.name, role1.name)
                    )
                except:
                    await ctx.send(_("```An Error occured```"))
            else:
                await ctx.send(
                    _("{} and {} are not registered as exclusive roles").format(
                        role1.name, role2.name
                    )
                )

    @commands.command()
    @checks.admin()
    async def listexclusives(self, ctx):
        """List all exclusive roles"""

        roles = await self.config.guild(ctx.guild).exclusives()
        embed = discord.Embed(title="Exclusivroles")
        text = ""
        if roles == []:
            text = _("No exclusive roles set")
        else:
            mentions = []
            for r in roles:
                mentions.append(
                    _("\n{} overwrites {}").format(
                        ctx.guild.get_role(r[0]).mention, ctx.guild.get_role(r[1]).mention,
                    )
                )
            text = "\n".join(mentions)
        embed.add_field(name=_("All exclusive role pairs:"), value=text)
        await ctx.send(embed=embed)

    @commands.command()
    @checks.admin()
    async def retroscan(self, ctx):
        """Scans the entire user list for roles that have been set as exclusive."""

        async with ctx.channel.typing():
            await ctx.send(_("``This may take a while...``"))
            roles = await self.config.guild(ctx.guild).exclusives()
            for r in roles:
                r_new = (ctx.guild.get_role(r[0]), ctx.guild.get_role(r[1]))
                if None in r_new:
                    self.log.warning(
                        f"One of the roles({r[0]},{r[1]}) was deleted from the guild. Removing config entry."
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
