from .botstatus import Botstatus


def setup(bot):
    bot.add_cog(Botstatus(bot))
