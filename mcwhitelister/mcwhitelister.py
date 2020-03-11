import urllib.request
import json
from redbot.core import commands, checks, Config


class McWhitelister(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=110320200153)
        default_guild = {"players": []}
        self.config.register_guild(**default_guild)

    @commands.group()
    async def whitelister(self, ctx):
        pass

    @whitelister.command(name="add")
    async def hinzufuegen(self, ctx, name: str):
        p_in_conf = await self.config.guild(ctx.guild).players()
        if not name in p_in_conf[1]:
            try:
                playerinfo = json.loads(
                    urllib.request.urlopen(
                        urllib.request.Request(
                            f"https://api.mojang.com/users/profiles/minecraft/{name}"
                        )
                    ).read()
                )
            except:
                await ctx.send("{} is not a valid username.".format(name))
                return
            await ctx.send("{} | {} | {}".format(playerinfo["id"], playerinfo["name"], name))

