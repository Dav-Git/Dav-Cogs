from .startupdetector import Mycog

def setup(bot):
    bot.add_cog(Mycog(bot))
