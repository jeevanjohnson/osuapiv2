import aiohttp
import asyncio
from typing import (
    Union
)
from objects import (
    Token, Gamemode, Player
)

class OsuApiV2:
    def __init__(self, client_id: int, client_secret: str, **kwargs) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: Token = None

        self.loop = kwargs.get('loop', asyncio.get_event_loop())

        self.session = aiohttp.ClientSession(loop=self.loop)
    
    async def get_access_token(self) -> None:
        url = 'https://osu.ppy.sh/oauth/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }

        async with self.session.post(url, data=data) as resp:
            if (
                not resp or 
                resp.status != 200 or 
                not (json := await resp.json())
            ):
                raise Exception(
                    "Couldn't Retrive token! Are your credentials correct?"
                )
        
        self.token = Token.from_api(json)

    async def get(self, url, **kwargs) -> Union[dict, bool]:
        async with self.session.get(url, **kwargs) as _resp:
            resp = _resp
            json = await resp.json()

        if (
            not resp or 
            resp.status != 200 or
            not json
        ):
            return
        
        return json

    async def get_me(self, mode: Gamemode = Gamemode.std) -> Union[Player, bool]:
        if not self.token:
            await self.get_access_token()
        
        if self.token.expired:
            await self.get_access_token()

        url = f'https://osu.ppy.sh/api/v2/me/{mode.value}'
        json = await self.get(url, headers = self.token.headers)
        if not json:
            return
            
        return Player.from_api(json)
    
    async def get_profile(
        self, userid: int, 
        mode: Gamemode = Gamemode.std
    ) -> Union[Player, bool]:
        if not self.token:
            await self.get_access_token()
        
        if self.token.expired:
            await self.get_access_token()

        url = ('https://osu.ppy.sh/api/v2'
               f'/users/{userid}/{mode.value}')
        json = await self.get(url, headers = self.token.headers)
        if not json:
            return
            
        return Player.from_api(json)