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
    GPT_5_4 = "gpt-5.4"
    GPT_5_4_MINI = "gpt-5.4-mini"
    GPT_5 = "gpt-5"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4_1_NANO = "gpt-4.1-nano"

    # Mistral
    MISTRAL_LARGE = "mistral-large-latest"
    MISTRAL_SMALL = "mistral-small-latest"

    # DeepSeek
    DEEPSEEK_V3 = "deepseek-chat"
    DEEPSEEK_R1 = "deepseek-reasoner"

class SpendLimitAction(str, Enum):
    WARN = "warn"
    BLOCK = "block"

MODEL_PROVIDER_MAP = {
    Model.CLAUDE_SONNET: Provider.ANTHROPIC,
    Model.CLAUDE_OPUS: Provider.ANTHROPIC,
    Model.CLAUDE_HAIKU: Provider.ANTHROPIC,
    Model.GPT_5_4: Provider.OPENAI,
    Model.GPT_5_4_MINI: Provider.OPENAI,
    Model.GPT_5: Provider.OPENAI,
    Model.GPT_4O: Provider.OPENAI,
    Model.GPT_4O_MINI: Provider.OPENAI,
    Model.GPT_4_1: Provider.OPENAI,
    Model.GPT_4_1_MINI: Provider.OPENAI,
    Model.GPT_4_1_NANO: Provider.OPENAI,
    Model.MISTRAL_LARGE: Provider.MISTRAL,
    Model.MISTRAL_SMALL: Provider.MISTRAL,
    Model.DEEPSEEK_V3: Provider.DEEPSEEK,
    Model.DEEPSEEK_R1: Provider.DEEPSEEK,
}

def get_provider_from_model(model: str) -> Provider:
    try:
        return MODEL_PROVIDER_MAP[Model(model)]
    except ValueError:
        raise ValueError(f"Unsupported model: {model}")