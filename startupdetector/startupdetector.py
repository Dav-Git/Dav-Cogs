import datetime

import discord
import asyncio
import os
import logging

from redbot.core import checks, commands
from redbot.core.data_manager import cog_data_path
from redbot.core.i18n import Translator, cog_i18


class StartupDetector(commands.Cog):
    """Startupdetector"""
    
    def __init__(self, bot):
        self.bot=bot
        delta = datetime.datetime.utcnow() - self.bot.uptime
        if delta.seconds < 120:
            self.sendmsg()
        else:
            self.sendmsg()
    
    async def sendmsg(self, ctx: commands.Context):
        destinations = await ctx.bot.get_owner_notification_destinations()
        for destination in destinations:
            try:
                await destination.send("The Bot just started.")
            except:
                pass
        return
        
