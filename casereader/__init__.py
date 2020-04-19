from .casereader import CaseReader


def setup(bot):
    cog = CaseReader(bot)
    bot.add_cog(cog)
