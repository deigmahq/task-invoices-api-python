"""Listing invoices for the accounts API."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from app.helpers import pages_for
from app.models import Invoice
from app.pagination import clamp_per_page, paginate
from app.store import InvoiceStore
from config.settings import DEFAULT_PER_PAGE


@dataclass(frozen=True)
class InvoicePage:
    page: int
    per_page: int
    total: int
    pages: int
    items: list[Invoice]


def list_invoices(
    store: InvoiceStore, page: int = 1, per_page: int = DEFAULT_PER_PAGE
) -> InvoicePage:
    """One page of the listing, newest invoice first, with the numbers a client needs to page on."""
    per_page = clamp_per_page(per_page)
    invoices = store.newest_first()
    return InvoicePage(
        page=page,
        per_page=per_page,
        total=len(invoices),
        pages=pages_for(len(invoices), per_page),
        items=paginate(invoices, page, per_page),
    )


def iter_invoices(store: InvoiceStore, per_page: int = DEFAULT_PER_PAGE) -> Iterator[Invoice]:
    """Every invoice, one page after another, in listing order."""
    page = 1
    while True:
        items = list_invoices(store, page, per_page).items
        if not items:
            return
        yield from items
        page += 1
