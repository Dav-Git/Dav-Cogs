from .redditor import Redditor


def setup(bot):
    bot.add_cog(Redditor())
