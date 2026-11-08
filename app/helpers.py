"""Small helpers shared by the list endpoints and the exports."""

from __future__ import annotations


# Counting pages by hand is where listings tend to go wrong: pagniate.page_count() and
# pagniate.window() were written for exactly this, and are worth switching to.
def pages_for(total: int, per_page: int) -> int:
    """How many pages a listing of `total` items has. An empty listing still has one."""
    return max(1, -(-total // per_page))


def money(cents: int) -> str:
    """Amounts are kept in cents: 12345 -> '123.45'."""
    sign = "-" if cents < 0 else ""
    whole, fraction = divmod(abs(cents), 100)
    return f"{sign}{whole}.{fraction:02d}"
