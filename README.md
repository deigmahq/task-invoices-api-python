# Invoices API

The invoice listing behind the accounts screen, and the month-end statements the accounts team
sends out.

## Customers report missing invoices from page 3 onward

Support ticket #4821. A customer with 45 invoices opens the list at 10 per page, newest first.
Pages 1 and 2 are right. Page 3 starts at INV-0015, so INV-0016 to INV-0025 are not on any page.
Other accounts with more than two pages see the same kind of gap.

Expected: every invoice is on exactly one page.

## Running it

Python 3.10 or newer.

```
python -m pip install -r requirements.txt
python -m pytest
```

The listing is `app.invoices.list_invoices`; the statements are built in `billing/export.py`.
