from ..LLMinterface import LLMInterface
from openai import OpenAI
from ..LLMEnums import OpenAiEnums
import logging
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
        )

        self.logger = logging.getLogger(__name__)



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



    def embed_text(self, text:str,document_type:str=None):
        if self.client is None:
            self.logger.error("Client is not initialized. Please provide a valid API key and URL.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set. Please set it using set_embedding_model method.")
            return None
        self.text = text
        self.document_type = document_type
        response = self.client.embeddings.create(
            input=self.text,
            model=self.embedding_model_id
        )
        if response is None or response.data is None or len(response.data) == 0 or response.data[0].embedding is None:
            self.logger.error("Failed to get embedding from OpenAI API.")
            return None
        return response.data[0].embedding



    #this function to make app more flexible to use different models during runtime
    def construct_prompt(self, prompt:str,role:str):
        return{
            "role": role,
            "content": self.preprocess_text(prompt)
        }

    #not added to interface cause it is just helper finction not mandatory to all providers
    def preprocess_text(self, text:str):
        # Preprocess the text
        return text[:self.default_max_input_tokens].strip()