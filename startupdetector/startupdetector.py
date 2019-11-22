from redbot.core import commands, checks, Config
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS, start_adding_reactions
import datetime



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
        
