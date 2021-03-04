# unfinished class, missing many features of what the Xbox API can offer
# TODO: implement models

from xbox.webapi.api.provider.baseprovider import BaseProvider

class ClubsProvider(BaseProvider):
    CLUBS_URL = "https://clubhub.xboxlive.com"
    HEADERS_CLUB = {'x-xbl-contract-version': '4'}

    async def get_clubs(self, club_ids, **kwargs):
        """
        Get information about the clubs provided.
        Args:
            club_ids: list of ids of clubs
        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = f"{self.PROFILE_URL}/clubs/batch/decoration/profile"
        post_data = {"Ids": [int(club_id) for club_id in club_ids]}

        resp = await self.client.session.post(
            url, json=post_data, headers=self.HEADERS_CLUB, **kwargs
        
        )
        resp.raise_for_status()
        return await resp.text()

    async def get_club(self, club_id, **kwargs):
        """
        Get information about a club.
        Args:
            club_id: id of club
        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = f"{self.PROFILE_URL}/clubs/Ids({club_id})/decoration/settings"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_CLUB, **kwargs
        )
        resp.raise_for_status()
        return await resp.text()

    async def get_club_user_presence(self, club_id, **kwargs):
        """
        Gets details about (at most) the last 1000 members active within a club.
        Args:
            club_id: id of club
        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """

        url = f"{self.PROFILE_URL}/clubs/Ids({club_id})/decoration/clubpresence"
        resp = await self.client.session.get(
            url, headers=self.HEADERS_CLUB, **kwargs
        )
        resp.raise_for_status()
        return await resp.text()