from .VectorDBEnums import VectorDBEnums
from stores.vectordb.providers.QdrantDBProvider import QdrantDBProvider
from stores.vectordb.providers.PGVectorProvider import PGVectorProvider
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker
class VectorDBProvidersFactory:
    def __init__(self,config: dict ,db_client:sessionmaker =None):
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client
    def create(self,provider_name:str):
        if provider_name == VectorDBEnums.QDRANT.value:
            return QdrantDBProvider (
                db_client=self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH),
                distance_method=self.config.VECTOR_DB_DISTANCE_METRIC,
                default_vector_size=self.config.EMBEDDING_MODLE_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )
        elif provider_name == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METRIC,
                default_vector_size=self.config.EMBEDDING_MODLE_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD,
            )

        return None