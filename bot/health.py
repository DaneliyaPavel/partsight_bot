from __future__ import annotations

from aiohttp import web


async def ok(request: web.Request) -> web.Response:
    """Return status response."""
    return web.json_response({"status": "ok"})


def create_app() -> web.Application:
    """Create aiohttp application with health route."""
    app = web.Application()
    app.router.add_get("/health", ok)
    return app
