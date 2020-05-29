from .rolesyncer import RoleSyncer


def setup(bot):
    bot.add_cog(RoleSyncer(bot))
