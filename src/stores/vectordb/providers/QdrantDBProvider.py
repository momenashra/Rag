from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import VectorDBEnums,DistanceTypeEnum
import logging
from qdrant_client import QdrantClient,models
from typing import List


class QdrantDBProvider(VectorDBInterface):
    def __init__(self, db_path: str,distance_method:str):
        
        self.db_path = db_path
        self.distance_method = None
        self.client = None

        if distance_method == DistanceTypeEnum.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceTypeEnum.EUCLIDEAN.value:
            self.distance_method = models.Distance.EUCLIDEAN
        elif distance_method == DistanceTypeEnum.DOT.value:
            self.distance_method = models.Distance.DOT
        else:
            raise ValueError(f"Invalid distance method: {distance_method}")
        

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client=None

    def is_collection_exists(self, collection_name: str):
         return self.client.collection_exists(collection_name=collection_name)



    def list_all_collections(self) :
        return self.client.get_collections()
        

    def get_collection_info(self, collection_name: str) :
        return self.client.get_collection(collection_name=collection_name)

    
    def delete_collection(self, collection_name: str) :
        if self.client.collection_exists(collection_name=collection_name):
            return self.client.delete_collection(collection_name=collection_name) 
   



    def create_collection(self, collection_name: str, embedding_dimension: int, do_reset:bool =False) :
        self.logger.info(f"Creating new Qdrant collection: {collection_name}")

        if do_reset:
           _= self.client.delete_collection(collection_name=collection_name)

        if not self.client.collection_exists(collection_name=collection_name):
            self.logger.info(f"Creating new Qdrant collection: {collection_name}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_dimension,
                    distance=self.distance_method
                )
            )
            self.logger.info(f"Created new Qdrant collection: {collection_name}")

            return True
        return False

    def insert_one (self, 
                    collection_name: str, text: str, 
                    vector: List, metadata: dict =None 
                    , record_id :str =None):
        if self.client.collection_exists(collection_name=collection_name):
            try:
                _= self.client.upload_records(
                    collection_name=collection_name,
                    records=[models.Record(
                        id=[record_id],
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )],
                )
            except Exception as e:
                self.logger.error(f"Error inserting record: {e}")
                return False
            
            return True
        
        self.logger.warning(f"Collection {collection_name} does not exist.")
        return False



    def insert_many (self, 
                     collection_name: str, texts: List , 
                     vectors: List , metadata: List =None , 
                     record_ids :List =None , batch_size:int =50):
        
        if metadata is None:
            metadata = [None] * len(vectors)
        if record_ids is None:
            record_ids = list(range(0,len(vectors)))

        for i in range(0, len(vectors), batch_size):
            batch_end=i+batch_size
            batch_vectors = vectors[i:batch_end]
            batch_texts = texts[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]
        
        batch_records= [
                    models.Record(
                        id=batch_record_ids[x],
                        vector=batch_vectors[x],
                        payload={
                            "text": batch_texts[x],
                            "metadata": batch_metadata[x]
                        }
                    )
                for x in range(len(batch_vectors))
            ]
        try:
            _= self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records
                )
        except Exception as e:
            self.logger.error(f"Error inserting records: {e}")
            return False
        
        return True

    def search_by_vector(self, 
                        collection_name: str, vector: List, 
                        limit: int = 5) :
        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )