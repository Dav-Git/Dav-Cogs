from .forcenick import ForceNick


async def setup(bot):
    cog = ForceNick(bot)
    await cog.initialize()
    bot.add_cog(cog)
