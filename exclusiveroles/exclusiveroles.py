import discord
from redbot.core import commands


class ExclusiveRoles(commands.Cog):
    """Exclusive Roles"""
    
    def __init__(self, bot):
        self.bot=bot
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        await self.test()
        return
    
    async def test(self):
        channel = self. bot.get_channel(630051748634951742)
        await channel.send("Test successfull")
