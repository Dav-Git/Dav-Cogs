from redbot.core.commands import Converter, ConversionError, BadArgument

VALID_STORAGE_TYPES = ["JSON", "TXT"]


class StorageTypeConverter(Converter):
    async def convert(self, ctx, argument: str):
        if argument.upper() in VALID_STORAGE_TYPES:
            return argument.upper()
        else:
            raise BadArgument()
