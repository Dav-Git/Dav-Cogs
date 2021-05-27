import asyncio
import string
from random import choice
from typing import Optional

import discord
from redbot.core import Config, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Roomer", __file__)


@cog_i18n(_)
class Roomer(commands.Cog):
    __version__ = "1.0.1"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        # Thanks Sinbad! And Trusty in whose cogs I found this.
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        pass  # This cog stores no EUD

    def __init__(self, bot):
        self.config = Config.get_conf(self, identifier=300620201743, force_registration=True)
        default_guild = {
            "auto_channels": None,
            "name": "general",
            "auto": False,
            "pstart": None,
            "pcat": None,
            "pchannels": {},
            "private": False,
            "private_textchannels_enabled": False,
            "private_textchannels": {},
        }
        self.config.register_guild(**default_guild)
        self.config.register_global(notification=0)
        self.invoiceConfig = None
        bot.loop.create_task(self.initialize(bot))

    async def initialize(self, bot):
        await bot.wait_until_red_ready()
        self._maybe_get_invoice_config(bot)
        await self._send_pending_owner_notifications(bot)

    # region listeners

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        settings = await self.config.guild(member.guild).all()
        # Some config cleanup for older versions here
        try:
            if settings["category"]:
                await self.config.guild(member.guild).category.clear()
        except KeyError:
            pass
        await self._autoroom_listener(settings, member, before.channel, after.channel)
        await self._privatevc_listener(settings, member, before.channel)

    # region autoroom listener

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

    # endregion autoroom listener

    # region privatevc listener

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

    # endregion privatevc listener

    # endregion listeners

    @commands.admin()
    @commands.guild_only()
    @commands.group()
    async def roomer(self, ctx):
        """Roomer settings"""
        pass

    @commands.guild_only()
    @commands.group()
    async def vc(self, ctx):
        """Voicechannel commands."""
        pass

    @commands.guild_only()
    @commands.group()
    async def tc(self, ctx):
        """Textchannel commands."""
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
        if not channel.category:
            return await ctx.send(
                _(
                    "{channel} is not in a discord category. Auto-channels need to be part of a category for this feature to work properly."
                ).format(channel=channel.name)
            )
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

    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    @vc.command()
    async def create(self, ctx, public: Optional[bool] = False, *, name: str):
        """Create a private voicechannel."""
        data = await self.config.guild(ctx.guild).all()
        if data["private"]:
            try:
                if ctx.author.voice.channel.id == data["pstart"]:
                    key = await self._generate_key(data["pchannels"].keys())
                    if public:
                        ov = {
                            ctx.author: discord.PermissionOverwrite(
                                view_channel=True, connect=True, speak=True, manage_channels=True
                            )
                        }
                    else:
                        ov = {
                            ctx.guild.default_role: discord.PermissionOverwrite(
                                view_channel=True,
                                connect=False,
                                use_voice_activation=True,
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
                    try:
                        await self._send_key(ctx, key)
                    except KeyError:
                        await ctx.send(
                            _("Couldn't send the key to your private channel. Aborting...")
                        )
                        await ctx.autho.move_to(ctx.author.voice.channel)
                        await c.delete()
                        return
                else:
                    await self.sendNotInStartChannelMessage(ctx, data["pstart"])
            except AttributeError:
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
                try:
                    if ctx.author.voice.channel.id == data["pstart"]:
                        if key in data["pchannels"]:
                            await ctx.author.move_to(ctx.guild.get_channel(data["pchannels"][key]))
                    else:
                        await self.sendNotInStartChannelMessage(ctx, data["pstart"])
                except AttributeError:
                    await self.sendNotInStartChannelMessage(ctx, data["pstart"])
            else:
                await ctx.send(_("Private rooms are not enabled on this server."))

    @commands.guild_only()
    @vc.command()
    async def hidden(self, ctx: commands.Context, true_or_false: Optional[bool] = True):
        """Hide or unhide a voicechannel you own."""
        data = await self.config.guild(ctx.guild).pchannels()
        try:
            for key in data:
                if data[key] == ctx.author.voice.channel.id:
                    ov = ctx.author.voice.channel.overwrites
                    ov[ctx.guild.default_role] = discord.PermissionOverwrite(
                        view_channel=False, connect=False
                    )
                    if self.invoiceConfig:
                        ov[
                            ctx.guild.get_role(
                                await self.invoiceConfig.channel(ctx.author.voice.channel).role()
                            )
                        ] = discord.PermissionOverwrite(
                            view_channel=True, connect=True, speak=True
                        )
                    await ctx.author.voice.channel.edit(overwrites=ov)
            await ctx.tick()
            await ctx.send(_("VC has been hidden successfully."))
        except AttributeError:
            return await ctx.send(_("You need to be in a VC to do this."))

    async def _send_key(self, ctx, key):
        text = _(
            "The key to your private room is: ``{key}``\nGive this key to a friend and ask them to use ``{command}`` to join your private room."
        ).format(key=key, command=f"{ctx.clean_prefix}vc join {key}")
        if self.invoiceConfig:
            for i in range(10):
                try:
                    await ctx.guild.get_channel(
                        await self.invoiceConfig.channel(ctx.author.voice.channel).channel()
                    ).send(text)
                    break
                except:
                    await asyncio.sleep(2)
                if i == 9:
                    await self._send_key_dm(ctx.author, text)
        else:
            await self._send_key_dm(ctx.author, text)

    async def _send_key_dm(self, author, text):
        try:
            await author.send(text)
        except discord.Forbidden:
            raise KeyError

    # endregion privatevc

    # region privatetc

    @roomer.group()
    async def text(self, ctx):
        """Change settings for private text channels."""
        pass

    @text.command(name="enable")
    async def tc_enable(self, ctx):
        """Enable private text channels."""
        await self.config.guild(ctx.guild).private_textchannels_enabled.set(True)
        await ctx.send(_("Private text channels enabled."))

    @text.command(name="disable")
    async def tc_disable(self, ctx):
        """Enable private text channels."""
        await self.config.guild(ctx.guild).private_textchannels_enabled.set(False)
        await ctx.send(_("Private text channels disabled."))

    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    @tc.command(name="create")
    async def tc_create(self, ctx, public: Optional[bool] = False, *, name: str):
        """Create a private text channel."""
        data = await self.config.guild(ctx.guild).all()
        if data["private_textchannels_enabled"]:
            key = await self._generate_key(data["private_textchannels"].keys())
            ov = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False,
                    read_message_history=False,
                    read_messages=False,
                    send_messages=False,
                ),
                ctx.author: discord.PermissionOverwrite(
                    view_channel=True,
                    manage_channels=True,
                    manage_messages=True,
                    read_message_history=True,
                    read_messages=True,
                    send_messages=True,
                    send_tts_messages=True,
                ),
            }
            c = await ctx.guild.create_text_channel(
                name,
                overwrites=ov,
                category=ctx.guild.get_channel(data["pcat"]),
                reason=_("Private text channel"),
            )
            data["private_textchannels"][key] = c.id
            await self.config.guild(ctx.guild).pchannels.set(data["private_textchannels"])
            await self._send_private_textchannel_key(c, key, ctx.clean_prefix)
        else:
            await ctx.send(_("Private text channels are not enabled on this server."))

    @commands.max_concurrency(1, commands.BucketType.guild, wait=True)
    @tc.command(name="close")
    async def tc_close(self, ctx):
        """Close the current private text cannel."""
        async with self.config.guild(ctx.guild).private_textchannels() as textchannels:
            if ctx.channel.id in textchannels:
                await ctx.channel.delete(reason=_("Private text channel deleted."))
                del textchannels[ctx.channel.id]
            else:
                await ctx.send(_("Use this command in a private text channel."))

    @tc.command(name="join")
    async def tc_join(self, ctx, key: str):
        """Join a private text channel."""
        await ctx.message.delete()
        async with ctx.typing():
            data = await self.config.guild(ctx.guild).all()
            if data["private_textchannels_enabled"]:
                if key in data["private_textchannels"]:
                    await ctx.guild.get_channel(int(key)).set_permissions(
                        ctx.author,
                        read_message_history=True,
                        read_messages=True,
                        send_messages=True,
                        view_channel=True,
                    )
            else:
                await ctx.send(_("Private rooms are not enabled on this server."))

    async def _send_private_textchannel_key(
        self, channel: discord.TextChannel, key: str, clean_prefix
    ):
        m = await channel.send(
            _(
                "The key to this private text channel is: ``{key}``\nGive this key to a friend and ask them to use ``{command}`` to join your private room."
            ).format(key=key, command=f"{clean_prefix}tc join {key}")
        )
        try:
            await m.pin()
        except discord.Forbidden:
            pass

    # endregion privatetc

    # region helpers
    async def sendNotInStartChannelMessage(self, ctx, channel_id):
        await ctx.send(
            _("You must be in the voicechannel {vc} first.").format(
                vc=ctx.guild.get_channel(channel_id).mention
            )
        )

    def _maybe_get_invoice_config(self, bot):
        if bot.get_cog("InVoice"):
            self.invoiceConfig = bot.get_cog("InVoice").config

    async def _send_pending_owner_notifications(self, bot):
        if await self.config.notification() == 0:
            await bot.send_to_owners(
                "Roomer: If you are updating roomer you will need to redo your autoroom setup.\n\nThis is due to some backend storage changes to allow for multiple automated categories."
            )
            await self.config.notification.set(1)

    async def _generate_key(self, key_list_for_channel_type):
        while True:
            # This probably won't turn into an endless loop bceause it has more possibilities than discord allows channels per guild
            key = "".join(choice(string.ascii_lowercase + "0123456789") for i in range(16))
            if not (key in key_list_for_channel_type):
                return key

    # endregion helpers
