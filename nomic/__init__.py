from .nomic import NoMic

async def setup(bot):
    cog=NoMic()
    await cog.initialize()
    bot.add_cog(cog)
