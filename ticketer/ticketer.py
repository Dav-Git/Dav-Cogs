import discord
from typing import Optional
from redbot.core import commands, checks, Config


class Ticketer(commands.Cog):
    """Ticketer"""

    def __init__(self):
        self.config = Config.get_conf(self, 200730042020, force_registration=True)
        default_guild = {
            "channel": None,
            "current-ticket": 0,
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    @checks.admin()
    async def ticketer(self, ctx):
        """All ticketer settings."""
        pass

    @commands.group()
    async def ticket(self, ctx):
        """Manage a ticket."""
        pass

    @ticket.command()
    async def create(self, ctx, reason: Optional[str] = None):
        """Create a ticket."""
        await self.config.guild(ctx.guild).all()
