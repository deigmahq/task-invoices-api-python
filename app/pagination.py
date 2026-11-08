"""Paging for the list endpoints.

A listing is already in order when it gets here; this module only cuts one page out of it.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

from config.settings import DEFAULT_PER_PAGE, HEAD_PAGES, MAX_PER_PAGE

T = TypeVar("T")


def clamp_per_page(per_page: int) -> int:
    """The page size actually used: at least 1, at most MAX_PER_PAGE."""
    return max(1, min(per_page, MAX_PER_PAGE))


def paginate(items: Sequence[T], page: int, per_page: int = DEFAULT_PER_PAGE) -> list[T]:
    """The items on one page of an ordered listing. Pages count from 1."""
    if page < 1:
        raise ValueError("pages start at 1")
    per_page = clamp_per_page(per_page)

    if page <= HEAD_PAGES:
        # The newest pages: cut straight from the head of the listing.
        head = items[: HEAD_PAGES * per_page]
        return list(head[(page - 1) * per_page : page * per_page])

    # Older pages: leave the head out, then step to the page that was asked for.
    rest = items[HEAD_PAGES * per_page :]
    offset = (page - HEAD_PAGES) * per_page
    return list(rest[offset : offset + per_page])
