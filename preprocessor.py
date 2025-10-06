import re
from typing import Tuple
import dateparser

WHITESPACE_RE = re.compile(r"\s+")
DASH_RANGE_RE = re.compile(r"\b(\d{1,2})\s*[-–]\s*(\d{1,2})\s*(\w+)\s*(\d{4})\b", re.IGNORECASE)

def normalize_whitespace(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()

def normalize_currency_symbols(text: str) -> str:
    # Heuristic: Map common symbols to 3-letter hints (kept as hint for the LLM).
    text = text.replace("NZ$", " NZD ").replace("AU$", " AUD ")
    text = re.sub(r"(?<![A-Z])(\$)\s*", " AUD ", text)  # $ -> AUD (best-effort; can be overridden by model)
    return text

def normalize_date_ranges(text: str) -> str:
    """Try to make date ranges easier for the LLM by standardizing formats where possible.
    Converts patterns like '10 - 20 Jan 2026' → '10 Jan 2026 to 20 Jan 2026'.
    """
    def repl(m):
        d1, d2, month, year = m.groups()
        return f"{d1} {month} {year} to {d2} {month} {year}"
    return DASH_RANGE_RE.sub(repl, text)

def preprocess(text: str) -> str:
    text = normalize_whitespace(text)
    text = normalize_currency_symbols(text)
    text = normalize_date_ranges(text)
    return text
