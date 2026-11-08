from billing.export import build_statements, export_csv, upload_request
from config import settings


def test_one_statement_per_customer_with_their_latest_invoice(make_store):
    statements = build_statements(make_store(14), per_page=10)
    assert [(s.customer, s.latest_number, s.invoices, s.total_cents) for s in statements] == [
        ("Birch & Co", "INV-0014", 5, 40_000),
        ("Acme Ltd", "INV-0013", 5, 35_000),
        ("Cobalt GmbH", "INV-0012", 4, 30_000),
    ]


def test_the_csv_lists_customers_in_the_order_they_first_turn_up(make_store):
    assert export_csv(make_store(14), per_page=10) == (
        "customer,latest_invoice,invoices,total\n"
        "Birch & Co,INV-0014,5,400.00\n"
        "Acme Ltd,INV-0013,5,350.00\n"
        "Cobalt GmbH,INV-0012,4,300.00\n"
    )


def test_the_upload_carries_the_csv_and_the_provider_credentials(make_store):
    request = upload_request(make_store(14), per_page=10)
    assert request["method"] == "POST"
    assert str(request["url"]).startswith(settings.INVOICE_PROVIDER_URL)
    assert request["headers"] == {
        "Authorization": f"Bearer {settings.INVOICE_PROVIDER_KEY}",
        "Content-Type": "text/csv",
    }
    assert request["body"] == export_csv(make_store(14), per_page=10)
