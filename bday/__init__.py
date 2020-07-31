from .bday import Bday


async def setup(bot):
    cog = Bday(bot)
    bot.add_cog(cog)
    await cog.initialize()
