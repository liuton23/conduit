from app.models.enums import Model

PRICING = {
    Model.CLAUDE_SONNET: {"input": 0.003, "output": 0.015},
    Model.CLAUDE_OPUS: {"input": 0.015, "output": 0.075},
    Model.CLAUDE_HAIKU: {"input": 0.00025, "output": 0.00125},
    Model.GPT_4O: {"input": 0.005, "output": 0.015},
    Model.GPT_4O_MINI: {"input": 0.00015, "output": 0.0006},
}

def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    try:
        model_enum = Model(model)
        pricing = PRICING.get(model_enum, {"input": 0.0, "output": 0.0})
    except ValueError:
        pricing = {"input": 0.0, "output": 0.0}
    
    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]
    return round(input_cost + output_cost, 6)