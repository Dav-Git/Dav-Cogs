from .casereader import CaseReader

__red_end_user_data_statement__ = "This cog does not store end user data."


def setup(bot):
    cog = CaseReader(bot)
    bot.add_cog(cog)
