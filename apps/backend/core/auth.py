from __future__ import annotations

from functools import lru_cache

from core.setup import configure_auth0


@lru_cache(maxsize=1)
def get_auth0():
    """Return a singleton Auth0 client for the process.

    This avoids trying to import an `auth0` variable from `main.py` (which would
    create circular imports) while still sharing the same configured instance
    across routers.
    """

    return configure_auth0()
