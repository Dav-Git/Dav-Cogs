from .caserelayer import CaseRelayer

__red_end_user_data_statement__ = "This cog does not store end user data."


def setup(bot):
    cog = CaseRelayer(bot)
    bot.add_cog(cog)
