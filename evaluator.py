from pathlib import Path
import json
from typing import Dict, Any
from schema import SupplierRate
from parser import parse_text_to_structured

def compare(expected: Dict[str, Any], got: Dict[str, Any]) -> Dict[str, float]:
    total = 0; correct = 0
    for k, v in expected.items():
        total += 1
        if str(got.get(k)).lower() == str(v).lower():
            correct += 1
    return {"field_accuracy": correct / max(total, 1)}

def run_case(model_id: str, text: str, expected: Dict[str, Any]):
    pred = parse_text_to_structured(text, model_id)
    metrics = compare(expected, pred)
    return pred, metrics

if __name__ == "__main__":
    # Example toy case
    text = "Ocean Breeze Resort - Gold Coast\nOcean View King | AUD 320 per night\nDates: Jan 10 - Jan 20, 2026\nExtras: Parking included. Free cancellation before Jan 5."
    expected = {
        "supplier_name": "Ocean Breeze Resort",
        "location": "Gold Coast, AU",
        "room_type": "Ocean View King",
        "price": 320,
        "currency": "AUD",
        "valid_from": "2026-01-10",
        "valid_to": "2026-01-20",
        "extras": ["parking", "free cancellation"]
    }
    model_id = "Qwen/Qwen2.5-1.5B-Instruct"
    pred, metrics = run_case(model_id, text, expected)
    print(json.dumps({"pred": pred, "metrics": metrics}, indent=2))
