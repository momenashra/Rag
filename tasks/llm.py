from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from functools import lru_cache


class LLM:
    def __init__(self, llm_type, llm_embedding_model_id: str, settings: dict={}):
        self.llm_type = llm_type
        self.llm_embedding_model_id = llm_embedding_model_id
        self.settings = settings
        self.embedding_model = self.load_embedding_model()


    @lru_cache(maxsize=1)
    def load_embedding_model(self):
        model = None

        if self.llm_type == "openai":
            model = OpenAIEmbeddings(model=self.llm_embedding_model_id,
                                     openai_api_key=self.settings.get("OPENAI_API_KEY"))
        elif self.llm_type == "huggingface":
            model = HuggingFaceEmbeddings(model_name=self.llm_embedding_model_id)
        else:
            raise ValueError(f"{self.llm_type} LLM is not supported")

        return model

    def get_embedding(self, texts: list):
        if isinstance(texts, str):
            texts = [texts]
        
        return self.model.embed_documents(texts)
