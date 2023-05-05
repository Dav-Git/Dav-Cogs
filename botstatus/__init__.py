from .botstatus import Botstatus
from pathlib import Path
import json

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot):
    cog = Botstatus(bot)
    await bot.add_cog(cog)
    cog.init()
