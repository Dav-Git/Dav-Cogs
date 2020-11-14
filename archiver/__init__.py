from .archiver import Archiver


def setup(bot):
    bot.add_cog(Archiver())