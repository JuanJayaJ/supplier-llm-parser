from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date
import re

class SupplierRate(BaseModel):
    supplier_name: str = Field(..., description="Supplier or property name, e.g., 'Luxury Stay Hotel'")
    location: str = Field(..., description="City + country/region if known, e.g., 'Queenstown, NZ'")
    room_type: str = Field(..., description="Room or product type, e.g., 'Deluxe Suite'")
    price: float = Field(..., ge=0, description="Price as a number, e.g., 250.0")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO-like 3-letter currency code, e.g., 'AUD', 'NZD'")
    valid_from: str = Field(..., description="Start date of validity in ISO format YYYY-MM-DD")
    valid_to: str = Field(..., description="End date of validity in ISO format YYYY-MM-DD")
    extras: List[str] = Field(default_factory=list, description="Free-form extras like ['breakfast','parking']")

    @field_validator('currency')
    @classmethod
    def uppercase_currency(cls, v: str) -> str:
        v = v.strip().upper()
        if not re.match(r'^[A-Z]{3}$', v):
            raise ValueError('currency must be a 3-letter code, e.g., AUD or NZD')
        return v
