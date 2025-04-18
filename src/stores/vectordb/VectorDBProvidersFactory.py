from .VectorDBEnums import VectorDBEnums,DistanceTypeEnum
from stores.vectordb.providers.QdrantDBProvider import QdrantDBProvider
from controllers.BaseController import BaseController

class VectorDBProvidersFactory:
    def __init__(self,config: dict ):
        self.config = config
        self.base_controller = BaseController()
    
    def create(self,provider_name:str):
        if provider_name == VectorDBEnums.QDRANT.value:
            return QdrantDBProvider (
                db_path=self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH),
                distance_method=self.config.VECTOR_dB_DISTANCE_METRIC,
            )

        return None