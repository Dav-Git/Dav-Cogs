import json
import urllib.request

from redbot.core import Config, checks, commands


class McWhitelister(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=110320200153)
        default_guild = {"players": [(None, None, None)]}
        self.config.register_guild(**default_guild)

    @commands.group()
    async def whitelister(self, ctx):
        pass

    @whitelister.command(name="add")
    async def hinzufuegen(self, ctx, name: str):
        p_in_conf = await self.config.guild(ctx.guild).players()
        for e in p_in_conf:
            if not name in e:
                try:
                    playerinfo = json.loads(
                        urllib.request.urlopen(
                            urllib.request.Request(
                                "https://api.mojang.com/users/profiles/minecraft/{}".format(name)
                            )
                        ).read()
                    )
                except:
                    await ctx.send("{} is not a valid username.".format(name))
                    return
                await ctx.send("{} | {} | {}".format(playerinfo["id"], playerinfo["name"], name))
                with open("/home/discbot/whitelist.json", "w+") as json_file:
                    file = json.load(json_file)
                    file.append({"uuid": playerinfo["id"], "name": playerinfo["name"]})
                    json.dump(file, json_file)
