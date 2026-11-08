"""The records the service handles."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Invoice:
    number: str
    customer: str
    issued_on: date
    amount_cents: int
