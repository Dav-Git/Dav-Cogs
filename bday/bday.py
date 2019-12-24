import discord
from redbot.core import commands, checks
from time import sleep


class Bday(commands.Cog):
    """Exclusive Roles"""
    
    def __init__(self):
        pass

   @commands.command()
   @checks.has_permissions()
   async def birthday(self, ctx, u: discord.Member):
       await u.add_roles(ctx.guild.get_role(657943577065947157))
       sleep(86400)
       await u.remove_roles(ctx.guild.get_role(657943577065947157))
