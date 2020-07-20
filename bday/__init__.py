from .bday import Bday


def setup(bot):
    cog = Bday(bot)
    bot.add_cog(cog)
    cog.initialize()
