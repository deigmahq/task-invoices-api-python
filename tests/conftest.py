from __future__ import annotations

from collections.abc import Callable
from datetime import date, timedelta

import pytest

from app.models import Invoice
from app.store import InvoiceStore

CUSTOMERS = ["Acme Ltd", "Birch & Co", "Cobalt GmbH"]


@pytest.fixture
def make_store() -> Callable[[int], InvoiceStore]:
    """A store of `count` invoices: INV-0001 upwards, one a day, customers in turn."""

    def build(count: int) -> InvoiceStore:
        store = InvoiceStore()
        for k in range(1, count + 1):
            store.add(
                Invoice(
                    number=f"INV-{k:04d}",
                    customer=CUSTOMERS[(k - 1) % len(CUSTOMERS)],
                    issued_on=date(2026, 3, 1) + timedelta(days=k - 1),
                    amount_cents=1000 * k,
                )
            )
        return store

    return build
