"""
Xbox Live Client

Basic factory that stores :class:`XboxLiveLanguage`, User authorization data
and available `Providers`
"""
import aiohttp
import asyncio
import logging

from xbox.webapi.api.provider.eds import EDSProvider
from xbox.webapi.api.provider.cqs import CQSProvider
from xbox.webapi.api.provider.lists import ListsProvider
from xbox.webapi.api.provider.profile import ProfileProvider
from xbox.webapi.api.provider.achievements import AchievementsProvider
from xbox.webapi.api.provider.usersearch import UserSearchProvider
from xbox.webapi.api.provider.gameclips import GameclipProvider
from xbox.webapi.api.provider.people import PeopleProvider
from xbox.webapi.api.provider.presence import PresenceProvider
from xbox.webapi.api.provider.message import MessageProvider
from xbox.webapi.api.provider.userstats import UserStatsProvider
from xbox.webapi.api.provider.screenshots import ScreenshotsProvider
from xbox.webapi.api.provider.titlehub import TitlehubProvider
from xbox.webapi.api.provider.account import AccountProvider
from xbox.webapi.api.provider.clubs import ClubProvider
from xbox.webapi.api.language import XboxLiveLanguage

log = logging.getLogger('xbox.api')

class XboxLiveClient(object):
    def __init__(self, userhash, auth_token, xuid, language=XboxLiveLanguage.United_States):
        authorization_header = {'Authorization': 'XBL3.0 x=%s;%s' % (userhash, auth_token)}
        self._session = aiohttp.ClientSession(headers=authorization_header)

        if isinstance(xuid, str):
            self._xuid = int(xuid)
        elif isinstance(xuid, int):
            self._xuid = xuid
        else:
            raise ValueError("Xuid was passed in wrong format, neither int nor string")

        self._lang = language

        self.eds = EDSProvider(self)
        self.cqs = CQSProvider(self)
        self.lists = ListsProvider(self)
        self.profile = ProfileProvider(self)
        self.achievements = AchievementsProvider(self)
        self.usersearch = UserSearchProvider(self)
        self.gameclips = GameclipProvider(self)
        self.people = PeopleProvider(self)
        self.presence = PresenceProvider(self)
        self.message = MessageProvider(self)
        self.userstats = UserStatsProvider(self)
        self.screenshots = ScreenshotsProvider(self)
        self.titlehub = TitlehubProvider(self)
        self.account = AccountProvider(self)
        self.club = ClubProvider(self)

    async def close(self):
        if not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    @property
    def xuid(self):
        """
        Gets the Xbox User ID

        Returns:
            int: Xbox User ID
        """
        return self._xuid

    @property
    def language(self):
        """
        Gets the active Xbox Live Language

        Returns:
            :class:`XboxLiveLanguage`: Active Xbox Live language
        """
        return self._lang

    @property
    def session(self):
        """
        Wrapper around requests session

        Returns:
            object: Instance of :class:`aiohttp.ClientSession` - Xbox Live Authorization header is set.
        """
        return self._session
