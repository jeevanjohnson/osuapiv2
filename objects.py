import time
from enum import Enum
from enum import unique
from typing import Union
from datetime import datetime

class Player:
    def __init__(self) -> None:
        self.avatar_url: str
        self.country_code: str
        self.default_proup: str
        self.id: int
        self.is_active: bool
        self.is_bot: bool
        self.is_deleted: bool
        self.is_online: bool
        self.is_supporter: bool
        self.last_visit: Union[datetime, bool]
        self.pm_friends_only: bool
        self.profile_colour: Union[str, bool]
        self.username: str
        self.comments_count: int
        self.cover_url: str
        self.discord: Union[str, bool]
        self.has_supporter: bool
        self.interest: Union[str, bool]
        self.join_date: datetime
        self.kudosu: dict
        self.location: Union[str, bool]
        self.max_blocks: int
        self.max_friends: int
        self.occupation: Union[str, bool]
        self.playmode: Gamemode
        self.playstyle: list[str]
        self.post_count: int
        self.profile_order: list[str]
        self.title: Union[str, bool]
        self.title_url: Union[str, bool]
        self.twitter: Union[str, bool]
        self.website: Union[str, bool]
        self.country: dict
        self.cover: dict
        self.account_history: list[dict, bool]
        self.active_tournament_banner: Union[list[dict], bool]
        self.badges: list[dict]
        self.beatmap_playcounts_count: int
        self.favourite_beatmapset_count: int
        self.follower_count: int
        self.graveyard_beatmapset_count: int
        self.groups: list[dict] # TODO look into


    @classmethod
    def from_api(cls, data: dict):
        p = cls()
        p.__dict__ = data

        last_visit: str = data['last_visit']
        join_date: str = data['join_date']
        gmode: str = data['playmode']

        p.last_visit = datetime.strptime(
            last_visit.split('+', 1)[0] + 'Z',
            '%Y-%m-%dT%H:%M:%SZ'
        )

        p.join_date = datetime.strptime(
            join_date.split('+', 1)[0] + 'Z',
            '%Y-%m-%dT%H:%M:%SZ'
        )

        p.playmode = Gamemode(gmode)
        
        return p

class Token:
    def __init__(self) -> None:
        self.token_type: str = None
        self.access_token: str = None
        self.expire_time: int = None
        self._expiration_date: float = None
        self.headers = {}
    
    @property
    def expired(self) -> bool:
        # Checks if token is expired
        return time.time() >= self._expiration_date

    @classmethod
    def from_api(cls, data: dict):
        creds = cls()

        creds.token_type = data['token_type']
        creds.access_token = data['access_token']
        creds.expire_time = data['expires_in']
        
        creds._expiration_date = time.time() + creds.expire_time
        creds.headers = {'Authorization': f'{creds.token_type} {creds.access_token}'}

        return creds


@unique
class Gamemode(Enum):
    std = 'osu'
    taiko = 'taiko'
    ctb = 'fruits'
    mania = 'mania'