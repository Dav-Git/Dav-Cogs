from redbot.core import commands, checks


class Prunecmd(commands.Cog):
    """Prunecmd"""

    def __init__(self):
        pass

    @commands.command()
    @checks.admin()
    async def prunecmd(self, ctx):

        """Prunes the discord member list of your guild. This will kick all users without a role and 24h inactivity."""

        await ctx.guild.prune_members(days=1, compute_prune_count=False, reason="Member prune")
        await ctx.send("The member list has been pruned successfully")
