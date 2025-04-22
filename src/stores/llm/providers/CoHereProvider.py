from ..LLMinterface import LLMInterface
import cohere
from ..LLMEnums import CoHereEnums ,DocumentTypeEnums
import logging

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


    def embed_text(self, text:str,document_type:str=None):
        if self.client is None:
            self.logger.error("Client is not initialized. Please provide a valid API key and URL.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set. Please set it using set_embedding_model method.")
            return None
        self.text = text
        self.document_type = document_type
        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnums.QUERY.value:
            input_type = CoHereEnums.QUERY.value
        response=self.client.embed(
        texts=[self.preprocess_text(text)], # Preprocess the text
        model=self.embedding_model_id,
        input_type=input_type,
        # output_dimension=1024,
        embedding_types=["float"],
        )
        # print(response.embeddings.float[0])
        if response is None or response.embeddings is None or response.embeddings.float is None:
            self.logger.error("Failed to get embedding from Cohere API.")
            return None
        return response.embeddings.float[0]


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