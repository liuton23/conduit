from enum import Enum

class Provider(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"

class Model(str, Enum):
    # Anthropic
    CLAUDE_SONNET = "claude-sonnet-4-6"
    CLAUDE_OPUS = "claude-opus-4-6"
    CLAUDE_HAIKU = "claude-haiku-4-5-20251001"

    # OpenAI
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"

MODEL_PROVIDER_MAP = {
    Model.CLAUDE_SONNET: Provider.ANTHROPIC,
    Model.CLAUDE_OPUS: Provider.ANTHROPIC,
    Model.CLAUDE_HAIKU: Provider.ANTHROPIC,
    Model.GPT_4O: Provider.OPENAI,
    Model.GPT_4O_MINI: Provider.OPENAI,
}

def get_provider_from_model(model: str) -> Provider:
    try:
        return MODEL_PROVIDER_MAP[Model(model)]
    except ValueError:
        raise ValueError(f"Unsupported model: {model}")