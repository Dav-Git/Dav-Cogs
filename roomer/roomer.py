from redbot.core import commands, Config, checks
import discord
from redbot.core.i18n import Translator, cog_i18n
from typing import Optional
from random import choice
import string

_ = Translator("Roomer", __file__)


@cog_i18n(_)
class Roomer(commands.Cog):
    """Multiple VC tools"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=300620201743, force_registration=True)
        default_guild = {
            "auto_channels": None,
            "name": "general",
            "auto": False,
            "pstart": None,
            "pcat": None,
            "pchannels": {},
            "private": False,
        }
        self.config.register_guild(**default_guild)
        self.config.register_global(notification=0)

    async def initialize(self, bot):
        notification = await self.config.notification()
        if notification == 0:
            await bot.send_to_owners(
                "Roomer: If you are updating roomer you will need to redo your autoroom setup.\n\nThis is due to some backend storage changes to allow for multiple automated categories."
            )
            await self.config.notification.set(1)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        settings = await self.config.guild(member.guild).all()
        # Some config cleanup here
        try:
            if settings["category"]:
                await self.config.guild(member.guild).category.clear()
        except KeyError:
            pass
        await self._autoroom_listener(settings, member, before.channel, after.channel)
        await self._privatevc_listener(settings, member, before.channel)

    async def _autoroom_listener(self, settings, member, before_channel, after_channel):
        if settings["auto"]:
            if settings["auto_channels"]:
                if after_channel:
                    await self._member_joined_auto_start_channel(settings, member, after_channel)
                if before_channel:
                    await self._maybe_delete_auto_channels(
                        settings, member, before_channel, after_channel
                    )

    async def _member_joined_auto_start_channel(self, settings, member, after_channel):
        if after_channel.id in settings["auto_channels"]:
            channel = await after_channel.category.create_voice_channel(
                settings["name"],
                overwrites=after_channel.overwrites,
                reason=_("Automated voicechannel creation."),
            )
            await member.move_to(channel, reason=_("Moved to automatically created channel."))

    async def _maybe_delete_auto_channels(self, settings, member, before_channel, after_channel):
        if len(before_channel.members) == 0:
            auto_categories = [
                member.guild.get_channel(c).category for c in settings["auto_channels"]
            ]
            if before_channel.id in settings["auto_channels"]:
                return
            elif before_channel.category in auto_categories:
                try:
                    await before_channel.delete(reason=_("Channel empty."))
                except discord.NotFound:
                    pass

    async def _privatevc_listener(self, settings, member, before_channel):
        if settings["private"]:
            if before_channel:
                if before_channel.id in settings["pchannels"].values():
                    if len(before_channel.members) == 0:
                        for key in settings["pchannels"]:
                            if settings["pchannels"][key] == before_channel.id:
                                ckey = key
                        del settings["pchannels"][ckey]
                        await self.config.guild(member.guild).pchannels.set(settings["pchannels"])
                        await before_channel.delete(reason=_("Private room empty."))

    @checks.admin()
    @commands.group()
    async def roomer(self, ctx):
        """Roomer settings"""
        pass

    @commands.group()
    async def vc(self, ctx):
        """Voicechannel commands."""
        pass

    # region auto
    @roomer.group()
    async def auto(self, ctx):
        """Automation settings."""
        pass

    @auto.command()
    async def enable(self, ctx):
        """Enable automatic voicechannel creation."""
        await self.config.guild(ctx.guild).auto.set(True)
        await ctx.send(_("Automatic voicechannel creation enabled."))

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

    @auto.group()
    async def channel(self, ctx):
        """Manage channels related to automated voicechannels."""
        pass

    @channel.command()
    async def add(self, ctx, *, channel: discord.VoiceChannel):
        """Add a start channel used for automatic voicechannels."""
        auto_channels = await self.config.guild(ctx.guild).auto_channels()
        if auto_channels is None:
            auto_channels = []
        auto_channels.append(channel.id)
        await self.config.guild(ctx.guild).auto_channels.set(auto_channels)
        await ctx.send(
            _("Startchannel used for automatic voicechannels added: {channel}").format(
                channel=channel.name
            )
        )

    @channel.command()
    async def remove(self, ctx, *, channel: discord.VoiceChannel):
        """Remove a start channel used for automatic voicechannels."""
        auto_channels = await self.config.guild(ctx.guild).auto_channels()
        auto_channels.remove(channel.id)
        await self.config.guild(ctx.guild).auto_channels.set(auto_channels)
        await ctx.send(
            _("Startchannel used for automatic voicechannels removed: {channel}").format(
                channel=channel.name
            )
        )

    # endregion auto

    # region privatevc
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
        await self.config.guild(ctx.guild).pcat.set(vc.category_id)
        await ctx.send(
            _(
                "Private starting channel set. Users can join this channel to use all features of private rooms.\nI recommend not allowing members to speak in this channel."
            )
        )

    @vc.command()
    async def create(self, ctx, public: Optional[bool] = False, *, name: str):
        """Create a private voicechannel."""
        data = await self.config.guild(ctx.guild).all()
        if data["private"]:
            if ctx.author.voice.channel:
                if ctx.author.voice.channel.id == data["pstart"]:
                    uniqueKeyFound = False
                    while not uniqueKeyFound:
                        # This probably won't turn into an endless loop bceause it has more possibilities than discord allows channels per guild
                        key = "".join(
                            choice(string.ascii_lowercase + "0123456789") for i in range(16)
                        )
                        if not (key in data["pchannels"]):
                            uniqueKeyFound = True
                    try:
                        await ctx.author.send(
                            _(
                                "The key to your private room is: ``{key}``\nGive this key to a friend and ask them to use ``{command}`` to join your private room."
                            ).format(key=key, command=f"{ctx.clean_prefix}vc join {key}")
                        )
                    except discord.Forbidden:
                        await ctx.send(
                            _("Couldn't send the key to your private channel via DM. Aborting...")
                        )
                        return
                    if public:
                        ov = {
                            ctx.author: discord.PermissionOverwrite(
                                view_channel=True, connect=True, speak=True, manage_channels=True
                            )
                        }
                    else:
                        ov = {
                            ctx.guild.default_role: discord.PermissionOverwrite(
                                view_channel=True, connect=False
                            ),
                            ctx.author: discord.PermissionOverwrite(
                                view_channel=True, connect=True, speak=True, manage_channels=True
                            ),
                        }
                    c = await ctx.guild.create_voice_channel(
                        name,
                        overwrites=ov,
                        category=ctx.guild.get_channel(data["pcat"]),
                        reason=_("Private room"),
                    )
                    await ctx.author.move_to(c, reason=_("Private channel."))
                    data["pchannels"][key] = c.id
                    await self.config.guild(ctx.guild).pchannels.set(data["pchannels"])
                else:
                    await self.sendNotInStartChannelMessage(ctx, data["pstart"])
            else:
                await self.sendNotInStartChannelMessage(ctx, data["pstart"])
        else:
            await ctx.send(_("Private rooms are not enabled on this server."))

    @commands.guild_only()
    @vc.command()
    async def join(self, ctx, key: str):
        """Join a private room."""
        await ctx.message.delete()
        async with ctx.typing():
            data = await self.config.guild(ctx.guild).all()
            if data["private"]:
                if ctx.author.voice:
                    if ctx.author.voice.channel:
                        if ctx.author.voice.channel.id == data["pstart"]:
                            if key in data["pchannels"]:
                                await ctx.author.move_to(
                                    ctx.guild.get_channel(data["pchannels"][key])
                                )
                        else:
                            await self.sendNotInStartChannelMessage(ctx, data["pstart"])
                    else:
                        await self.sendNotInStartChannelMessage(ctx, data["pstart"])
                else:
                    await self.sendNotInStartChannelMessage(ctx, data["pstart"])
            else:
                await ctx.send(_("Private rooms are not enabled on this server."))

    @commands.guild_only()
    @vc.command()
    async def hidden(self, ctx, true_or_false: Optional[bool] = True):
        """Hide or unhide a voicechannel you own."""
        data = await self.config.guild(ctx.guild).pchannels()
        if ctx.author.voice.channel:
            for key in data:
                if data[key] == ctx.author.voice.channel.id:
                    ov = {
                        ctx.guild.default_role: discord.PermissionOverwrite(
                            view_channel=False, connect=False
                        ),
                        ctx.author: discord.PermissionOverwrite(
                            view_channel=True, connect=True, speak=True, manage_channels=True
                        ),
                    }
                    await ctx.author.voice.channel.edit(overwrites=ov)

    # endregion privatevc

    # region helpers
    async def sendNotInStartChannelMessage(self, ctx, channel_id):
        await ctx.send(
            _("You must be in the voicechannel {vc} first.").format(
                vc=ctx.guild.get_channel(channel_id).mention
            )
        )

    # endregion helpers
