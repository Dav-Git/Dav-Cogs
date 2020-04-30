from .ticketer import Ticketer


def setup(bot):
    bot.add_cog(Ticketer())
