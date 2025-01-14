import aiohttp

from typing import Any, Literal

from app.configs import AppConfig


class ApiService:
    def __init__(
        self,
        config: AppConfig,
    ):
        self._config = config

    async def request(
        self,
        target_server: Literal["bot", "account"],
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE"],
        **kwargs: dict[Any, Any]
    ) -> dict[str, Any] | str:
        async with aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self._config.auth.secret_key}"
            }
        ) as session:
            if target_server == "bot":
                base_url = self._config.env.base_bot_api_url
            else:
                base_url = self._config.env.base_api_url
            try:
                async with session.request(
                    method=method,
                    url=base_url+endpoint,
                    **kwargs
                ) as response:
                    response.raise_for_status()
                    try:
                        return await response.json()
                    except aiohttp.ContentTypeError:
                        return await response.text()

            except aiohttp.ClientError as exc:
                raise aiohttp.ClientError(
                    f"Request error for {endpoint}: {exc}"
                ) from exc
