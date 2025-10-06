import argparse, json, sys
from pathlib import Path
from typing import Any, Dict
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from rich import print as rprint

from preprocessor import preprocess
from postprocessor import extract_json_block, repair_json, postprocess
from schema import SupplierRate

FEW_SHOT_EXAMPLES = [
    {
        "input": "Luxury Stay Hotel, Queenstown\nDeluxe Suite $250/night (NZD). Valid: 1–15 Dec 2025. Includes breakfast, WiFi.",
        "output": {
            "supplier_name": "Luxury Stay Hotel",
            "location": "Queenstown, NZ",
            "room_type": "Deluxe Suite",
            "price": 250,
            "currency": "NZD",
            "valid_from": "2025-12-01",
            "valid_to": "2025-12-15",
            "extras": ["breakfast", "wifi"]
        }
    },
    {
        "input": "Ocean Breeze Resort - Gold Coast\nOcean View King | AUD 320 per night\nDates: Jan 10 - Jan 20, 2026\nExtras: Parking included. Free cancellation before Jan 5.",
        "output": {
            "supplier_name": "Ocean Breeze Resort",
            "location": "Gold Coast, AU",
            "room_type": "Ocean View King",
            "price": 320,
            "currency": "AUD",
            "valid_from": "2026-01-10",
            "valid_to": "2026-01-20",
            "extras": ["parking", "free cancellation"]
        }
    }
]

def build_prompt(text: str) -> str:
    instructions = (
        "You are a tourism supplier parser.\n"
        "Extract the following fields and return ONLY valid JSON (no prose):\n"
        "supplier_name (string), location (string), room_type (string), price (number), currency (3-letter code), "
        "valid_from (YYYY-MM-DD), valid_to (YYYY-MM-DD), extras (list of strings).\n\n"
        "Use the examples to match the exact JSON shape.\n\n"
    )
    shots = []
    for ex in FEW_SHOT_EXAMPLES:
        shots.append(f"### Example Input\n{ex['input']}\n### Example Output\n{json.dumps(ex['output'], ensure_ascii=False)}")
    return instructions + "\n\n".join(shots) + f"\n\n### Now Parse This\n{text}\n### JSON Output\n"

def generate(model_id: str, prompt: str, max_new_tokens: int = 512, temperature: float = 0.1) -> str:
    tok = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    mdl = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", trust_remote_code=True)
    pipe = pipeline("text-generation", model=mdl, tokenizer=tok)
    out = pipe(prompt, max_new_tokens=max_new_tokens, do_sample=temperature > 0, temperature=temperature)
    return out[0]["generated_text"][len(prompt):] if out and len(out) > 0 else ""

def parse_text_to_structured(raw_text: str, model_id: str) -> Dict[str, Any]:
    cleaned = preprocess(raw_text)
    prompt = build_prompt(cleaned)

    # First attempt
    llm_text = generate(model_id, prompt)
    json_text = extract_json_block(llm_text)
    json_text = repair_json(json_text)

    try:
        data = json.loads(json_text)
        obj = SupplierRate(**data)
        return postprocess(obj.model_dump(), raw_text)
    except Exception as e:
        # Retry with stricter instruction
        strict_prompt = prompt + "\nReturn ONLY JSON. No comments. No backticks. No extra text.\n"
        llm_text = generate(model_id, strict_prompt, temperature=0.0)
        json_text = repair_json(extract_json_block(llm_text))
        data = json.loads(json_text)
        obj = SupplierRate(**data)
        return postprocess(obj.model_dump(), raw_text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_path", type=str, help="Path to unstructured text file")
    ap.add_argument("--model-id", type=str, default="Qwen/Qwen2.5-1.5B-Instruct", help="HF model id to use")
    ap.add_argument("--max-new-tokens", type=int, default=512)
    ap.add_argument("--temperature", type=float, default=0.1)
    args = ap.parse_args()

    raw = Path(args.input_path).read_text(encoding="utf-8")
    rprint(f"[bold]Parsing:[/bold] {args.input_path} using [cyan]{args.model_id}[/cyan]...")
    result = parse_text_to_structured(raw, args.model_id)
    rprint("[green]OK[/green] → ", result)

    out_path = Path("outputs") / (Path(args.input_path).stem + ".json")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    rprint(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
