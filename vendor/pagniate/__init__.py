"""Page arithmetic: window() and page_count()."""

from __future__ import annotations

__version__ = "0.2.0"
__all__ = ["page_count", "window"]


def page_count(total: int, per_page: int) -> int:
    """Pages needed for `total` items, at least one."""
    if per_page < 1:
        raise ValueError("per_page starts at 1")
    return max(1, -(-total // per_page))


def window(page: int, per_page: int) -> slice:
    """The slice of an ordered sequence that holds `page`. Pages count from 1."""
    if page < 1 or per_page < 1:
        raise ValueError("page and per_page start at 1")
    start = (page - 1) * per_page
    return slice(start, start + per_page)
