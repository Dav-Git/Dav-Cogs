from .supporter import Supporter
from pathlib import Path
import json

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


async def setup(bot):
    cog = Supporter(bot)
    await cog.register_casetypes()
    bot.add_cog(cog)
