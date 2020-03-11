from .mcwhitelister import McWhitelister


def setup(bot):
    bot.add_cog(McWhitelister())
