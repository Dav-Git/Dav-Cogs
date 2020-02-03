from .persistentmute import PersistentMute

def setup(bot):
    bot.add_cog(PersistentMute())