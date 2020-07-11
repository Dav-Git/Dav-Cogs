from .check import Check


def setup(bot):
    bot.add_cog(Check(bot))
