from .bday import Bday

__red_end_user_data_statement__ = "This cog stores user IDs for the duration of approximately 24h to revoke the birthday role 24h after assignment."


def setup(bot):
    cog = Bday(bot)
    bot.add_cog(cog)
    cog.initialize()
