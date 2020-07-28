import discord
from redbot.core import commands, Config, checks
from typing import Optional
from redbot.core.i18n import cog_i18n, Translator

_ = Translator("nomic", __file__)


@cog_i18n(_)
class NoMic(commands.Cog):
    """#No-mic manager"""
    async def initialize(self):
        await self.bot.send_to_owners(
            "Nomic is outdated and will be removed in August 2020. Use InVoice (<https://github.com/zephyrkul/FluffyCogs/>) instead."
        )

    def __init__(self):
        self.config = Config.get_conf(self, identifier=889, force_registration=True)
        default = {"channels": {}}
        self.config.register_global(**default)
        self.vc = None

    async def initialize(self):
        self.vc = await self.config.channels()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Show #no-mic if member in VC
        try:
            if self.vc[str(member.guild.id)]:
                if after.channel:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.read_messages = True
                    if type(self.vc[str(member.guild.id)]) == int:
                        await member.guild.get_channel(
                            self.vc[str(member.guild.id)]
                        ).set_permissions(member, overwrite=overwrite)
                    elif type(self.vc[str(member.guild.id)]) == dict:
                        try:
                            await member.guild.get_channel(
                                self.vc[str(member.guild.id)][str(after.channel.id)]
                            ).set_permissions(member, overwrite=overwrite)
                        except KeyError:
                            pass
                        if before.channel:
                            try:
                                await member.guild.get_channel(
                                    self.vc[str(member.guild.id)][str(before.channel.id)]
                                ).set_permissions(member, overwrite=None)
                            except KeyError:
                                pass
                else:
                    if type(self.vc[str(member.guild.id)]) == int:
                        await member.guild.get_channel(
                            self.vc[str(member.guild.id)]
                        ).set_permissions(member, overwrite=None)
                    elif type(self.vc[str(member.guild.id)]) == dict:
                        try:
                            await member.guild.get_channel(
                                self.vc[str(member.guild.id)][str(before.channel.id)]
                            ).set_permissions(member, overwrite=None)
                        except KeyError:
                            pass
        except KeyError:
            pass

    @checks.admin()
    @commands.group()
    async def nomicset(self, ctx):
        """Chanege NoMic settings. WARNING: If you are changing settings from a different mode than what you are using currently, this WILL overwrite your settings."""
        pass

    @nomicset.command()
    async def simple(self, ctx, channel: Optional[discord.TextChannel]):
        """Define the channel used as no-mic channel on the entire server.\n\nLeave empty to disable."""
        async with self.config.channels() as channels:
            if channel:
                channels[str(ctx.guild.id)] = channel.id
            else:
                channels[str(ctx.guild.id)] = None
        await ctx.send(
            _("No-mic channel set to {channel}.").format(
                channel=channel.mention if channel else "disabled"
            )
        )
        self.vc = await self.config.channels()

    @nomicset.command()
    async def map(self, ctx, vc: discord.VoiceChannel, textchannel: Optional[discord.TextChannel]):
        """Map voicechannels to their own seperate no-mic channels. \n\nLeave out textchannel to disable for a specified vc."""
        async with self.config.channels() as channels:
            if type(channels[str(ctx.guild.id)]) == int:
                channels[str(ctx.guild.id)] = {}
            if textchannel:
                channels[str(ctx.guild.id)][str(vc.id)] = textchannel.id
            else:
                channels[str(ctx.guild.id)][str(vc.id)] = None
        await ctx.send(
            _("No-mic for {vc} set to {textchannel}.").format(
                vc=vc.name, textchannel=textchannel.mention if textchannel else "``None``"
            )
        )
        self.vc = await self.config.channels()

    @nomicset.command()
    async def mapping(self, ctx):
        """Show the current nomic mapping."""
        if type(self.vc[str(ctx.guild.id)]) == int:
            await ctx.send(_("NoMic is currently in simple mode."))
        else:
            message = []
            for key in self.vc[str(ctx.guild.id)]:
                message.append(
                    "{vc} --> {textchannel}".format(
                        vc=ctx.guild.get_channel(int(key)).name,
                        textchannel=ctx.guild.get_channel(
                            int(self.vc[str(ctx.guild.id)][key])
                        ).mention,
                    )
                )
            sendable = _("Current mapping\n") + "\n".join(message)
            await ctx.send(sendable)
