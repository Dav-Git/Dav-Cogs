from redbot.core import commands, Config, checks
import discord
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Roomer", __file__)


@cog_i18n(_)
class Roomer(commands.Cog):
    """Multiple VC tools"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=300620201743, force_registration=True)
        default_guild = {
            "category": None,
            "name": "general",
            "auto": False,
            "pstart": None,
            "private": False,
        }
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        settings = await self.config.guild(member.guild).all()
        if settings["auto"]:  # Autoroom stuff
            dellist = []
            for vc in member.guild.get_channel(settings["category"]).voice_channels:
                if not vc.members:
                    dellist.append(vc)
            if len(dellist) > 1:
                dellist.remove(dellist[0])
                for vc in dellist:
                    await vc.delete(reason=_("Channel empty."))
            channel_needed = True
            for vc in member.guild.get_channel(settings["category"]).voice_channels:
                if not vc.members:
                    channel_needed = False
            if channel_needed:
                await member.guild.create_voice_channel(
                    name=settings["name"],
                    category=member.guild.get_channel(settings["category"]),
                    reason=_("A channel is needed."),
                )

    @checks.admin()
    @commands.group()
    async def roomer(self, ctx):
        """Roomer settings"""
        pass

    # region auto
    @roomer.group()
    async def auto(self, ctx):
        """Automation settings."""
        pass

    @auto.command()
    async def enable(self, ctx):
        """Enable automatic voicechannel creation."""
        settings = await self.config.guild(ctx.guild).all()
        # Create a VC in case none exist.
        try:
            if not ctx.guild.get_channel(settings["category"]).voice_channels:
                await ctx.guild.create_voice_channel(
                    name=settings["name"],
                    category=ctx.guild.get_channel(settings["category"]),
                    reason=_("No channels exist. We need one for people to join though."),
                )
            await self.config.guild(ctx.guild).auto.set(True)
            await ctx.send(_("Automatic voicechannel creation enabled."))
        except:
            await ctx.send(
                _(
                    "Make sure you set a category with {command} and have at least one voicechannel in it."
                ).format(command=f"``{ctx.clean_prefix}roomer auto category [category-ID]``")
            )

    @auto.command()
    async def disable(self, ctx):
        """Disable automatic voicechannel creation."""
        await self.config.guild(ctx.guild).auto.set(True)
        await ctx.send(_("Automatic voicechannel creation disabled."))

    @auto.command()
    async def name(self, ctx, *, name: str):
        """Set the name that is used for automatically created voicechannels."""
        await self.config.guild(ctx.guild).name.set(name)
        await ctx.send(
            _("Automatically created voicechannels will now be named ``{name}``.").format(
                name=name
            )
        )

    @auto.command()
    async def category(self, ctx, *, category: discord.CategoryChannel):
        """Set the category used for automatic voicechannels."""
        await self.config.guild(ctx.guild).category.set(category.id)
        await ctx.send(
            _("Category used for automatic voicechannels set to: {category}").format(
                category=category.name
            )
        )

    # endregion auto

    # region private
    @roomer.group()
    async def private(self, ctx):
        """Change settings for private rooms"""
        pass

    @private.command(name="enable")
    async def penable(self, ctx):
        """Enable private rooms"""
        if await self.config.guild(ctx.guild).pstart():
            await self.config.guild(ctx.guild).private.set(True)
            await ctx.send(_("Private channels enabled."))
        else:
            await ctx.send(
                _("Set up a starting channel using {command} first.").format(
                    command=f"``{ctx.clean_prefix}roomer private startchannel``"
                )
            )

    @private.command(name="disable")
    async def pdisable(self, ctx):
        """Disable private rooms"""
        await self.config.guild(ctx.guild).private.set(False)
        await ctx.send(_("Private channels disabled."))

    @private.command()
    async def startchannel(self, ctx, vc: discord.VoiceChannel):
        """Set a channel that users will join to start using private rooms.\nI recommend not allowing talking permissions here."""
        await self.config.guild(ctx.guild).pstart.set(vc.id)
        await ctx.send(
            _(
                "Private starting channel set. USers can join this channel to use all features of private rooms.\nI recommend not allowing members to speak in this channel."
            )
        )

    # endregion private
