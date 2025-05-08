from ..LLMinterface import LLMInterface
from openai import OpenAI
from ..LLMEnums import OpenAiEnums
import logging
from typing import List,Union

class OpenAiprovider(LLMInterface):
    def __init__(self, api_key: str,api_url:str=None,
                        default_max_input_tokens:int=1000,
                        default_max_output_tokens:int=1000,
                        default_temperature:float=0.1):
        self.api_key = api_key
        self.api_url = api_url
        self.default_max_input_tokens = default_max_input_tokens
        self.default_max_output_tokens = default_max_output_tokens
        self.default_temperature = default_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_url if self.api_url and len(self.api_url) else None,
            )

        self.logger = logging.getLogger(__name__)

        self.enums = OpenAiEnums

    #this function to make app more flexible to use different models during runtime
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
        chat_history.append(self.construct_prompt(prompt=self.prompt,role=OpenAiEnums.USER.value))

        response=self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=chat_history,
                max_tokens=self.max_output_tokens,
                temperature=self.temperature
            )
        if response is None or response.choices is None or len(response.choices) == 0 or response.choices[0].message is None:
            self.logger.error("Failed to get generation from OpenAI API.")
            return None
        return response.choices[0].message.content



    def embed_text(self, text: Union[str, List[str]], document_type: str = None):
        if self.client is None:
            self.logger.error("Client is not initialized. Please provide a valid API key and URL.")
            return None
        if isinstance(text, str):
            text = [text]
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set. Please set it using set_embedding_model method.")
            return None

        # Preprocess each text individually
        preprocessed_texts = [self.preprocess_text(t) for t in text]

        response = self.client.embeddings.create(
            input=preprocessed_texts,
            model=self.embedding_model_id
        )
        if response is None or response.data is None or len(response.data) == 0 or response.data[0].embedding is None:
            self.logger.error("Failed to get embedding from OpenAI API.")
            return None
        return [rec.embedding for rec in response.data]

    # def rerank_search_result(self,query:str,documents:list):
    #     reranked_documents = self.client.rerank(
    #         model="rerank-english-v3.0",
    #         top_n=2,
    #         return_documents=True,
    #         query=query,
    #         documents=documents
    #     )
    #     extracted_results = []
    #     # Access the results from the V2RerankResponse object
    #     for item in reranked_documents.results:
    #         extracted_results.append({
    #             'document': item.document.text,
    #             'score': item.relevance_score
    #         })
        
    #     print(f"Reranked results: {extracted_results}")
    #     return extracted_results


    #this function to make app more flexible to use different models during runtime
    def construct_prompt(self, prompt:str,role:str):
        return{
            "role": role,
            "content": prompt
        }

    #not added to interface cause it is just helper finction not mandatory to all providers
    def preprocess_text(self, text:str):
        # Preprocess the text
        return text[:self.default_max_input_tokens]