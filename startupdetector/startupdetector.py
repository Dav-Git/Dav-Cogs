from redbot.core import commands
import datetime
import discord


class Mycog(commands.Cog):
    """My custom cog"""
    
    def __init__(self, bot):
        self.bot=bot
        delta = datetime.datetime.utcnow() - self.bot.uptime
        if delta.seconds < 120:
            sendmsg()
            
    async def sendmsg(self, ctx):
        destinations = await ctx.bot.get_owner_notification_destinations()
        for destination in destinations:
            try:
                await destination.send("The Bot just started.")
            except:
                pass
        return
        
