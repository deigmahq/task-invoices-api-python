"""Month-end statements for the accounts team."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass

from app.helpers import money
from app.invoices import iter_invoices
from app.store import InvoiceStore
from config import settings


@dataclass
class Statement:
    customer: str
    latest_number: str
    invoices: int
    total_cents: int


def build_statements(
    store: InvoiceStore, per_page: int = settings.DEFAULT_PER_PAGE
) -> list[Statement]:
    """One statement per customer, in the order customers first turn up in the listing.

    The listing is newest first, so the first invoice seen for a customer is their latest one, and
    that is the number the statement carries.
    """
    statements: dict[str, Statement] = {}
    for invoice in iter_invoices(store, per_page):
        statement = statements.get(invoice.customer)
        if statement is None:
            statements[invoice.customer] = Statement(
                customer=invoice.customer,
                latest_number=invoice.number,
                invoices=1,
                total_cents=invoice.amount_cents,
            )
        else:
            statement.invoices += 1
            statement.total_cents += invoice.amount_cents
    return list(statements.values())


def export_csv(store: InvoiceStore, per_page: int = settings.DEFAULT_PER_PAGE) -> str:
    """The statements as the CSV the accounts team opens."""
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["customer", "latest_invoice", "invoices", "total"])
    for statement in build_statements(store, per_page):
        writer.writerow(
            [
                statement.customer,
                statement.latest_number,
                statement.invoices,
                money(statement.total_cents),
            ]
        )
    return out.getvalue()


def upload_request(
    store: InvoiceStore, per_page: int = settings.DEFAULT_PER_PAGE
) -> dict[str, object]:
    """The request that hands the statements to the invoice provider.

    Only describes it; sending is the job runner's work.
    """
    return {
        "method": "POST",
        "url": f"{settings.INVOICE_PROVIDER_URL}/statements",
        "headers": {
            "Authorization": f"Bearer {settings.INVOICE_PROVIDER_KEY}",
            "Content-Type": "text/csv",
        },
        "body": export_csv(store, per_page),
    }
