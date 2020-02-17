from .botstatus import Botstatus


async def setup(bot):
    cog = Botstatus(bot)
    bot.add_cog(cog)
    cog.init()
