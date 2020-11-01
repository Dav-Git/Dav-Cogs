from .modlogstats import ModLogStats


def setup(bot):
    bot.add_cog(ModLogStats())