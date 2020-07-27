from xbox.webapi.api.provider.baseprovider import BaseProvider

# unfinished class, missing many features of what the Xbox API can offer

class ClubsProvider(BaseProvider):
    PROFILE_URL = "https://clubhub.xboxlive.com"
    HEADERS_CLUB = {
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
        super(ClubsProvider, self).__init__(client)
        self.HEADERS_CLUB.update({'Accept-Language': self.client.language.locale})

    async def get_clubs(self, club_ids: list()):
        """
        Get information about the clubs provided.
        Args:
            club_ids: list of ids of clubs
        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        post_data = {
            "Ids": [int(club_id) for club_id in club_ids]
        }
        url = self.PROFILE_URL + "/clubs/batch/decoration/profile"
        return await self.client.session.post(url, json=post_data, headers=self.HEADERS_CLUB)

    async def get_club(self, club_id):
        """
        Get information about a club.
        Args:
            club_id: id of club
        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = self.PROFILE_URL + "/clubs/Ids(%s)/decoration/settings" % club_id
        return await self.client.session.get(url, headers=self.HEADERS_CLUB)

    async def get_club_user_presence(self, club_id):
        """
        Gets details about (at most) the last 1000 members active within a club.
        Args:
            club_id: id of club
        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """

        url = self.PROFILE_URL + "/clubs/Ids(%s)/decoration/clubpresence" % club_id
        return await self.client.session.get(url, headers=self.HEADERS_CLUB)