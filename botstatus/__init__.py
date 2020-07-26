from .botstatus import Botstatus

__red_end_user_data_statement__ = "This cog does not store end user data."


async def setup(bot):
    cog = Botstatus(bot)
    bot.add_cog(cog)
    cog.init()
