from .nomic import NoMic


async def setup(bot):
    cog = NoMic(bot)
    await cog.initialize()
    bot.add_cog(cog)
