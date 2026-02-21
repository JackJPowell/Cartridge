import os
import time
from typing import Any, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
IGDB_API_URL = "https://api.igdb.com/v4"


class IGDBClient:
    def __init__(self):
        self.client_id: str = os.environ.get("IGDB_CLIENT_ID", "")
        self.client_secret: str = os.environ.get("IGDB_CLIENT_SECRET", "")
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0.0

    async def _get_access_token(self) -> str:
        if self._access_token and time.time() < self._token_expires_at:
            return self._access_token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TWITCH_TOKEN_URL,
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                },
            )
            response.raise_for_status()
            data = response.json()
            self._access_token = data["access_token"]
            # Refresh a minute before actual expiry to avoid edge cases
            self._token_expires_at = time.time() + data.get("expires_in", 3600) - 60
            return self._access_token

    async def _headers(self) -> dict:
        token = await self._get_access_token()
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}",
        }

    async def search_game(self, query: str) -> list[dict[str, Any]]:
        headers = await self._headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{IGDB_API_URL}/games",
                headers=headers,
                content=f'search "{query}"; fields id,name,summary,cover,rating,first_release_date,genres,platforms,involved_companies; limit 10;',
            )
            response.raise_for_status()
            return response.json()

    async def get_game_by_id(self, igdb_id: int) -> Optional[dict[str, Any]]:
        headers = await self._headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{IGDB_API_URL}/games",
                headers=headers,
                content=f"where id = {igdb_id}; fields id,name,summary,cover,rating,first_release_date,genres,platforms,involved_companies; limit 1;",
            )
            response.raise_for_status()
            results = response.json()
            return results[0] if results else None


igdb_client = IGDBClient()
