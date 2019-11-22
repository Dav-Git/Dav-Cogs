from .startupdetector import StartupDetector

def setup(bot):
    bot.add_cog(Mycog(bot))
