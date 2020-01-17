"""
Peaplehub

Get Userprofiles by XUID or Gamertag
"""
from xbox.webapi.api.provider.baseprovider import BaseProvider


class PeoplehubProvider(BaseProvider):
    PROFILE_URL = "https://peoplehub.xboxlive.com"
    HEADERS_PEOPLEHUB = {
        'x-xbl-contract-version': '3',
        'Accept-Language': 'overwrite in __init__'
    }
    SEPARATOR = ","

    def __init__(self, client):
        """
        Initialize Baseclass, set 'Accept-Language' header from client instance

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super(PeoplehubProvider, self).__init__(client)
        self.HEADERS_PEOPLEHUB.update({'Accept-Language': self.client.language.locale})

    async def get_peoplehubs(self, xuid_list, decorations=None):
        """
        Get peoplehub info for list of xuids

        Args:
            xuid_list (list): List of xuids
            decorations (list): List of decorations

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.PROFILE_URL + "/users/xuid(%s)/people/batch" % self.client.xuid
        if decorations:
            url = url + "/decoration/" + ",".join(decorations)
        json = {'xuids': [int(xuid) for xuid in xuid_list]}
        return await self.client.session.post(url, json=json, headers=self.HEADERS_PEOPLEHUB)


class PeoplehubDecorations(object):
    """
    Peoplehub Decorations, used as parameter for Peoplehub API
    """
    PREFERRED_COLOR = "preferredcolor"
    PRESENCE_DETAIL = "presenceDetail"
