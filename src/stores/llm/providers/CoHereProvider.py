from ..LLMinterface import LLMInterface
import cohere
from ..LLMEnums import CoHereEnums ,DocumentTypeEnums
import logging
from typing import List,Union
import asyncio
class CoHereProvider(LLMInterface):
    def __init__(self, api_key: str,
                        default_max_input_tokens:int=1000,
                        default_max_output_tokens:int=1000,
                        default_temperature:float=0.1):
        self.api_key = api_key
        self.default_max_input_tokens = default_max_input_tokens
        self.default_max_output_tokens = default_max_output_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.ClientV2(
            api_key=self.api_key,
        )
        self.logger = logging.getLogger(__name__)

        self.enums = CoHereEnums

    def set_generation_model(self, model_id:str):
        self.generation_model_id = model_id


    def set_embedding_model(self, model_id:str,embedding_size:int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size



    def generate_text(self, prompt:str , chat_history:list=[],
                      max_output_tokens:int=None, 
                      temperature:float=None):
        if self.client is None:
            self.logger.error("Client is not initialized. Please provide a valid API key and URL.")
            return None
        self.prompt = prompt
        self.max_output_tokens = max_output_tokens if max_output_tokens else self.default_max_output_tokens
        self.temperature = temperature if temperature else self.default_temperature
        chat_history.append(self.construct_prompt(prompt=self.prompt,role=CoHereEnums.USER.value))

        response=self.client.chat(
                model=self.generation_model_id,
                messages=chat_history,
                max_tokens=self.max_output_tokens,
                temperature=self.temperature
            )
        if response is None or response.message is None   or response.message.content[0] is None or response.message.content[0].text is None :
            self.logger.error("Failed to get generation from Cohere API.")
            return None
        return response.message.content[0].text


    def embed_text(self, text:Union[str, List[str]], document_type:str=None, batch_size:int=50):
        if self.client is None:
            self.logger.error("Client is not initialized. Please provide a valid API key and URL.")
            return None

        if isinstance(text, str):
            text = [text]

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set. Please set it using set_embedding_model method.")
            return None

        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnums.QUERY.value:
            input_type = CoHereEnums.QUERY.value

        all_embeddings = []

        for i in range(0, len(text), batch_size):
            batch_texts = text[i:i+batch_size]
            try:
                response = self.client.embed(
                    texts=[self.preprocess_text(t) for t in batch_texts],
                    model=self.embedding_model_id,
                    input_type=input_type,
                    embedding_types=["float"],
                )
            except Exception as e:
                self.logger.error(f"Error calling Cohere API for batch: {e}")
                continue

            if response is None or response.embeddings is None or response.embeddings.float is None:
                self.logger.error("Failed to get embeddings for batch from Cohere API.")
                continue

            all_embeddings.extend(response.embeddings.float)

            # OPTIONAL: Sleep to avoid API rate limit
            # asyncio.sleep(1)  # Small pause

        return all_embeddings


    #this function to make app more flexible to use different models during runtime
    def construct_prompt(self, prompt:str,role:str):
        return{
            "role": role,
            "content": prompt
        }


    #not added to interface cause it is just helper finction not mandatory to all providers
    def preprocess_text(self, text:str):
        # Preprocess the text
        return text[:self.default_max_input_tokens].strip()