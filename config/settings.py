"""Settings the service reads when it starts."""

import os

# Listing
DEFAULT_PER_PAGE = 25
MAX_PER_PAGE = 100
# The newest pages are the ones nearly every client asks for, so they are cut straight from the
# head of the listing without looking at the rest of it.
HEAD_PAGES = 2

# Invoice provider (month-end statement uploads)
INVOICE_PROVIDER_URL = os.environ.get(
    "INVOICE_PROVIDER_URL", "https://api.invoice-provider.example/v2"
)
INVOICE_PROVIDER_KEY = "ivp_4c2d0fada04"
