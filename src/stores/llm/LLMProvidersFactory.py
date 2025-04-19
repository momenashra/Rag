from .LLMEnums import LLMEnums
from .providers import OpenAiprovider,CoHereProvider

class LLMProviderFactory:

    def __init__(self,config: dict ):
        self.config = config
    
    def create(self,provider_name:str):
        if provider_name == LLMEnums.OPENAI.value:
            return OpenAiprovider (
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_max_input_tokens=self.config.INPUT_DEFAULT_MAX_CARACTERS,
                default_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPRATURE,
            )
        elif provider_name == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_max_input_tokens=self.config.INPUT_DEFAULT_MAX_CARACTERS,
                default_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPRATURE,
            )
