from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    HUGGINGFACE = "HUGGINGFACE"


class OpenAiEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"