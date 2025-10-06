# LLM-Powered Unstructured → Structured Supplier Parser (Free & Open-Source)

Turn messy supplier descriptions (text) into validated JSON using **free Hugging Face models**, 
**Pydantic** schemas, and robustness layers (pre/post-processing, retries, JSON repair).

## Features (Improvement-First)
-  **Schema-first** with Pydantic
-  **Pre-processing**: normalize dates/prices/currency hints
-  **Post-processing**: currency mapping, extras splitting, JSON repair
-  **Retr+y & validation loop**: re-ask model if output invalid
-  **Synthetic data generator** for unstructured texts
-  **Evaluator** scaffold for simple metrics
-  **Totally free** (no OpenAI) – runs on CPU or Colab GPU

## Quickstart
```bash
# 1) Create venv 
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Create a few synthetic examples
python generator.py --n 5

# 4) Parse one example (choose any generated file path)
python parser.py examples/input_1.txt --model-id "Qwen/Qwen2.5-1.5B-Instruct"

# 5) See structured JSON
cat outputs/input_1.json
```

> **Tip:** If CPU is slow, run on **Google Colab** with GPU: upload the folder and run the same commands.

## Model Notes
Default is a small Instruct model to keep CPU-friendly: `Qwen/Qwen2.5-1.5B-Instruct`.
You can try other open models (heavier but better JSON adherence), e.g. `mistralai/Mistral-7B-Instruct-v0.2`.
Pass `--model-id` to override.

## Project Layout
```
supplier-llm-parser/
├─ parser.py          # main pipeline (prompt → model → validation → postprocess)
├─ schema.py          # Pydantic model of structured output
├─ preprocessor.py    # regex/text cleanup before LLM
├─ postprocessor.py   # currency mapping, extras splitting, JSON repair
├─ validator.py       # retry + validation utilities
├─ evaluator.py       # scaffold for running simple accuracy checks
├─ generator.py       # synthetic messy supplier text generator
├─ examples/          # unstructured inputs (generated here)
├─ outputs/           # structured JSON results
├─ requirements.txt
└─ README.md
```

## Roadmap
- [ ] Add grammar-constrained decoding (e.g., outlines/jsonformer) for stricter JSON
- [ ] Add FastAPI wrapper (`/parse`) for a production-like demo
- [ ] Build a tiny Streamlit UI for side-by-side (raw vs structured)
- [ ] Add more evaluation scenarios + field-wise scoring

---

**License:** MIT. Use at your own risk. Educational/demo purpose.
