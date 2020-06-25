import json
from pathlib import Path

import aiohttp
from discord import Embed
from redbot.core import Config, checks, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("McWhitelister", __file__)


@cog_i18n(_)
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
            with open(path) as json_file:
                file = json.load(json_file)
            for e in file:
                if e["uuid"] == p_in_conf[str(member.id)]["uuid"]:
                    del file[file.index(e)]
                    with open("{}whitelist.json".format(path), "w") as json_file:
                        json.dump(file, json_file, indent=4)
            del p_in_conf[str(member.id)]
            await self.config.guild(member.guild).players.set(p_in_conf)

    @commands.group()
    async def whitelister(self, ctx):
        pass

    @whitelister.command(name="add")
    async def hinzufuegen(self, ctx, name: str):
        path = await self.config.guild(ctx.guild).path_to_server()
        if path:
            with open(path) as json_file:
                file = json.load(json_file)
            whitelisted = False
            for e in file:
                if e["name"] == name:
                    whitelisted = True
                    await ctx.send(_("{} is already on the whitelist.").format(name))
            if not whitelisted:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(
                            "https://api.mojang.com/users/profiles/minecraft/{}".format(name)
                        ) as resp:
                            playerinfo = await resp.json()
                    p_in_conf = await self.config.guild(ctx.guild).players()
                    p_in_conf[ctx.author.id] = {
                        "uuid": playerinfo["id"],
                        "name": playerinfo["name"],
                    }
                    await self.config.guild(ctx.guild).players.set(p_in_conf)
                except:
                    await ctx.send(_("{} is not a valid username.").format(name))
                    return
                await ctx.send(
                    _("{} successfully whitelisted {}.").format(
                        ctx.author.mention, playerinfo["name"]
                    )
                )
                file.append({"uuid": playerinfo["id"], "name": playerinfo["name"]})
                with open(path, "w") as json_file:
                    json.dump(file, json_file, indent=4)
        else:
            await ctx.send(_("You need to set a path with ``[p]whitelister setup`` first."))

    @checks.is_owner()
    @whitelister.command()
    async def setup(self, ctx, path: str):
        """Set up the path to your minecraft server jar.
        It needs to lead to the folder that contains both the server jar and whitelist.json .

        Example on a linux system:
        ``[p]whitelister setup /home/user/mcserver/whitelist.json``"""
        p = Path(path)
        if p.exists():
            await self.config.guild(ctx.guild).path_to_server.set(path)
            await ctx.send(_("Path set to {}").format(path))
        else:
            await ctx.send(_("The whitelist.json could not be found at this path."))

    @checks.admin()
    @whitelister.command(name="list")
    async def liste(self, ctx):
        p_in_config = await self.config.guild(ctx.guild).players()
        outstr = []
        for e in p_in_config:
            outstr.append(
                "{} | {} \n".format(ctx.guild.get_member(int(e)).mention, p_in_config[e]["name"])
            )
        emb = Embed(title=_("Whielisted with whitelister:"))
        if len(p_in_config) == 0:
            emb.add_field(
                name=_("Whitelisted"), value=_("Nobody was whitelisted using whitelister yet.")
            )
        else:
            emb.add_field(name=_("Whitelisted"), value="".join(outstr))
        await ctx.send(embed=emb)
