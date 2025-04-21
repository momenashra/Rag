from abc import ABC ,abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from models.db_shemas import RetrivedData

class VectorDBInterface (ABC):
    """
    Abstract base class for Vector Database interface.
    """
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        """
        Check if a collection exists in the vector database.
        """
        pass
    

    @abstractmethod
    def list_all_collections(self) -> List:
        """
        List all collections in the vector database.
        """
        pass
    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        """
        Get information about a specific collection in the vector database.
        """
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool:
        """
        Delete a collection from the vector database.
        """
        pass




    @abstractmethod
    def create_collection(self, collection_name: str, embedding_dimension: int, do_reset:bool =False) :
        """
        Create a new collection in the vector database.
        """
        pass


    @abstractmethod
    def insert_one (self, 
                    collection_name: str, text: str, 
                    vector: List, metadata: dict =None , record_id :str =None):
        """
        Insert a single document into the vector database.
        """
        pass

    @abstractmethod
    def insert_many (self, 
                     collection_name: str, texts: List , 
                     vectors: List , metadata: List =None , 
                     record_ids :List =None , batch_size:int =50):
        """
        Insert multiple documents into the vector database.
        """
        pass
    
    @abstractmethod
    def search_by_vector(self, 
                        collection_name: str, vector: List, 
                        limit: int = 5) -> List[RetrivedData]:
        """
        Search for documents in the vector database using a vector.
        """
        pass