from .caserelayer import CaseRelayer


def setup(bot):
    cog = CaseRelayer(bot)
    bot.add_cog(cog)
