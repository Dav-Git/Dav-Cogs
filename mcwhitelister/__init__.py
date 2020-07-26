from .mcwhitelister import McWhitelister

__red_end_user_data_statement__ = "This cog stores end user data in order to allow it to whitelist players on a minecraft server. It stores minecraft player names(and user IDs) as well as discord user IDs."


def setup(bot):
    bot.add_cog(McWhitelister(bot))
