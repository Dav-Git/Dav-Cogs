from .supporter import Supporter


async def setup(bot):
    cog = Supporter(bot)
    await cog.register_casetypes()
    bot.add_cog(cog)
