from .exclusiveroles import ExclusiveRoles


def setup(bot):
    bot.add_cog(ExclusiveRoles(bot))
