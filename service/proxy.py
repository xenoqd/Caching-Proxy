import httpx
from typing import Optional


async def forward_request(
    method: str,
    url: str,
    headers: dict,
    body: Optional[bytes] = None,
):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            content=body,
        )

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "content": response.content,
    }
