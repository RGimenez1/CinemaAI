import httpx
import logging
from typing import Any, Dict


class OpenAPIRepository:
    async def make_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        params: Dict[str, Any] = None,
        body: Any = None,
    ) -> Any:
        """Make an API request based on the provided method, URL, headers, and optional parameters/body."""
        logging.info(
            f"Making {method.upper()} request to {url} with params {params} and body {body}"
        )
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method,
                    url,
                    headers=headers,
                    params=params if method == "get" else None,
                    json=body if method in ["post", "put", "patch"] else None,
                )
                response.raise_for_status()
                logging.info(
                    f"Received response with status code {response.status_code}"
                )
                return response.json()
            except httpx.RequestError as e:
                logging.error(f"Request failed: {e}")
                raise SystemExit(f"Request failed: {e}")
