from .httpcat import HttpCat


def setup(bot):
    bot.add_cog(HttpCat())
