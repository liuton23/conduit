import json
from pathlib import Path

PRICING_FILE = Path(__file__).parent.parent.parent / "pricing.json"

def load_pricing() -> dict:
    with open(PRICING_FILE) as f:
        data = json.load(f)
    return {k: v for k, v in data.items() if not k.startswith("_")}

PRICING = load_pricing()

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = PRICING.get(model, {"input": 0.0, "output": 0.0})
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    return round(input_cost + output_cost, 6)