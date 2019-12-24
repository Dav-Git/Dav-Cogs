import discord
from discord.ext import tasks
from redbot.core import commands, checks



class Bday(commands.Cog):
    """Bday"""
    
    def __init__(self,bot):
        self.rem_bday.start()
        
    def cog_unload(self):
        self.rem_bday.cancel()

    @commands.command()
    @checks.has_permissions()
    async def birthday(self, ctx, u: discord.Member):
        await u.add_roles(ctx.guild.get_role(657943577065947157))
        
    @tasks.loop(seconds=86400.0)
    async def rem_bday(self):
        role = self.bot.fetch_guild(332834024831582210).get_role(657943577065947157)
        for member in self.bot.fetch_guild(332834024831582210).members:
            if role in member.roles:
                member.remove_roles(role , reason="The birthday is over!")
        
