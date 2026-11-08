"""Where invoices are kept.

An in-memory book, so the service can be read and tested without a database. The real service sits
on one; the interface is the same.
"""

from __future__ import annotations

from collections.abc import Iterable

from app.models import Invoice


class InvoiceStore:
    def __init__(self, invoices: Iterable[Invoice] = ()) -> None:
        self._invoices: list[Invoice] = list(invoices)

    def add(self, invoice: Invoice) -> None:
        self._invoices.append(invoice)

    def newest_first(self) -> list[Invoice]:
        """Every invoice, newest first. Invoices from the same day go by number, highest first."""
        return sorted(self._invoices, key=lambda i: (i.issued_on, i.number), reverse=True)

    def __len__(self) -> int:
        return len(self._invoices)
