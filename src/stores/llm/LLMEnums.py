from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    HUGGINGFACE = "HUGGINGFACE"


class OpenAiEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"

class CoHereEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"
    DOCUMENT ="search_document"
    QUERY="search_query"

class DocumentTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"