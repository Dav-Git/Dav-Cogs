import json
import urllib.request

from discord import Embed
from redbot.core import Config, checks, commands


class McWhitelister(commands.Cog):
    def __init__(self):
        self.config = Config.get_conf(self, identifier=110320200153)
        default_guild = {"players": {}, "path_to_server": ""}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        p_in_conf = await self.config.guild(member.guild).players()
        if str(member.id) in p_in_conf:
            path = await self.config.guild(member.guild).path_to_server()
            with open("{}whitelist.json".format(path)) as json_file:
                file = json.load(json_file)
            for e in file:
                if e["uuid"] == p_in_conf[str(member.id)]["uuid"]:
                    del file[file.index(e)]
                    with open("{}whitelist.json".format(path), "w") as json_file:
                        json.dump(file, json_file, indent=4)
            del p_in_conf[member.id]
            await self.config.guild(member.guild).players.set(p_in_conf)

    @commands.group()
    async def whitelister(self, ctx):
        pass

    @whitelister.command(name="add")
    async def hinzufuegen(self, ctx, name: str):
        path = await self.config.guild(ctx.guild).path_to_server()
        if path:
            with open("{}whitelist.json".format(path)) as json_file:
                file = json.load(json_file)
            whitelisted = False
            for e in file:
                if e["name"] == name:
                    whitelisted = True
                    await ctx.send("{} is already on the whitelist.".format(name))
            if not whitelisted:
                try:
                    playerinfo = json.loads(
                        urllib.request.urlopen(
                            urllib.request.Request(
                                "https://api.mojang.com/users/profiles/minecraft/{}".format(name)
                            )
                        ).read()
                    )
                    p_in_conf = await self.config.guild(ctx.guild).players()
                    p_in_conf[ctx.author.id] = {
                        "uuid": playerinfo["id"],
                        "name": playerinfo["name"],
                    }
                    await self.config.guild(ctx.guild).players.set(p_in_conf)
                except:
                    await ctx.send("{} is not a valid username.".format(name))
                    return
                await ctx.send(
                    "{} successfully whitelisted {}.".format(
                        ctx.author.mention, playerinfo["name"]
                    )
                )
                file.append({"uuid": playerinfo["id"], "name": playerinfo["name"]})
                with open("{}whitelist.json".format(path), "w") as json_file:
                    json.dump(file, json_file, indent=4)
        else:
            await ctx.send("You need to set a path with ``[p]whitelister setup`` first.")

    @checks.admin()
    @whitelister.command()
    async def setup(self, ctx, path: str):
        """Set up the path to your minecraft server jar.
        It needs to lead to the folder that contains both the server jar and whitelist.json .

        Example on a linux system:
        ``[p]whitelister setup /home/user/mcserver/``"""
        await self.config.guild(ctx.guild).path_to_server.set(path)
        await ctx.send("Path set to {}".format(path))

    @checks.admin()
    @whitelister.command(name="list")
    async def liste(self, ctx):
        p_in_config = await self.config.guild(ctx.guild).players()
        outstr = []
        for e in p_in_config:
            outstr.append(
                "{} | {} \n".format(ctx.guild.get_member(int(e)).mention, p_in_config[e]["name"])
            )
        emb = Embed(title="Whielisted with whitelister:")
        if len(p_in_config) == 0:
            emb.add_field(
                name="Whitelisted", value="Nobody was whitelisted using whitelister yet."
            )
        else:
            emb.add_field(name="Whitelisted", value="".join(outstr))
        await ctx.send(embed=emb)

