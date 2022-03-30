from typing import Optional

import discord


class AltMarkerException(Exception):
    """Base exception for AltMarker"""

    def __init__(
        self,
        message: str,
        *,
        member: Optional[discord.Member] = None,
        alt: Optional[discord.Member] = None,
    ):
        self.message = message
        self.member = member
        self.alt = alt
        super().__init__(self, message)


class AltAlreadyRegistered(AltMarkerException):
    """Raised when a given alt has already been registered for a member"""


class AltNotRegistered(AltMarkerException):
    """Raised when a given alt is not registered for a member"""
