import json
import re
from typing import List, Dict

CURRENCY_CANON = {
    'AUD': 'AUD',
    'AU$': 'AUD',
    '$': 'AUD',      
    'NZD': 'NZD',
    'NZ$': 'NZD'
}

def ensure_currency_code(value: str, raw_text: str) -> str:
    v = (value or '').strip().upper()
    if v in CURRENCY_CANON:
        return CURRENCY_CANON[v]
    # Try to infer from raw text
    if ' NZD ' in raw_text or 'New Zealand' in raw_text or 'NZ ' in raw_text:
        return 'NZD'
    return 'AUD'  # default fallback

EXTRAS_TOKENS = [
    'breakfast', 'wifi', 'parking', 'airport pickup', 'spa', 'pool',
    'free cancellation', 'non-refundable', 'min stay', 'late checkout'
]

def split_extras(extras_field) -> List[str]:
    if isinstance(extras_field, list):
        items = extras_field
    else:
        items = re.split(r",|;|\n|\||/", str(extras_field or ''))
    norm = []
    txt = ' ' + ' '.join(items).lower() + ' '
    for token in EXTRAS_TOKENS:
        if f' {token} ' in txt:
            norm.append(token)
    return sorted(set(norm))

def extract_json_block(text: str) -> str:
    """Return substring from first '{' to last '}' to increase chance of valid JSON."""
    first = text.find('{')
    last = text.rfind('}')
    if first != -1 and last != -1 and last > first:
        return text[first:last+1]
    return text

def repair_json(text: str) -> str:
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    # Replace single quotes with double quotes (best-effort)
    if text.count('"') == 0 and text.count("'") > 0:
        text = text.replace("'", '"')
    return text

def postprocess(parsed: Dict, raw_text: str) -> Dict:
    parsed = dict(parsed)
    parsed['currency'] = ensure_currency_code(parsed.get('currency', ''), raw_text)
    parsed['extras'] = split_extras(parsed.get('extras', []))
    return parsed
