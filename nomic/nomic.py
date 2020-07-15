import discord
from redbot.core import commands, Config, checks


class NoMic(commands.Cog):
    """#No-mic manager"""
    def __init__(self):
        self.config=self.Config.get_conf(self,identifier=889,force_registration=True)
        default={"channels":{}}
        self.config.register_default(**default)
        self.vc=None

    async def initialize(self):
        self.vc = await self.config.channels()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Show #no-mic if member in VC
        try:
            if self.vc[member.guild.id]:
                if after.channel:
                    overwrite = discord.PermissionOverwrite()
                    overwrite.send_messages = True
                    overwrite.read_messages = True
                    await member.guild.get_channel(self.vc[str(member.guild.id)]).set_permissions(
                        member, overwrite=overwrite
                    )
                else:
                    await member.guild.get_channel(self.vc[str(member.guild.id)]).set_permissions(
                        member, overwrite=None
                    )
        except KeyError:
            pass

    @checks.admin()
    @commands.command()
    async def setnomic(self,ctx,channel: discord.TextChannel):
        """Define the channel used as no-mic channel.\n\nLeave empty to disable."""
        async with self.config.channels() as channels:
            channels[str(ctx.guild.id)] = channel.id
        await ctx.send("No-mic channel set to {channel}".format(channel=channel.memtion))
        self.vc = await self.config.channels()
            
