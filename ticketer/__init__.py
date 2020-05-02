from .ticketer import Ticketer


async def setup(bot):
    cog = Ticketer()
    await cog.register_casetypes()
    bot.add_cog(cog)
