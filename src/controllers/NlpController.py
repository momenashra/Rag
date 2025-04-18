from .BaseController import BaseController
from models import ResponseSignals
from fastapi import HTTPException

from models import ProcessingEnums
from models.db_shemas import DataChunk, Project
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnums
import json
class NlpController(BaseController):
    def __init__(self,vector_db_client,embedding_client,generation_client):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        
    def create_collection_name(self,project_id:str):
        collection_name = f"collection_{project_id}"
        return collection_name
    

    def reset_vector_db_collection(self, project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return  self.vector_db_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        print(f"[VectorDB] Getting collection info for {collection_name}")
        try:
            collection_info= self.vector_db_client.get_collection_info(collection_name=collection_name)
        except ValueError as e:
            # Log if needed
            print(f"[VectorDB Error] {e}")
            # Return HTTP 404 instead of crashing
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")
        return json.loads(
            json.dumps( collection_info, default=lambda o: o.__dict__ ) 
        )
    
    def index_into_vector_db (self,project:Project,processed_chunks:List [DataChunk],chunks_ids:list[int], do_reset:bool =False):

        # get the collection name from the project id
        collection_name = self.create_collection_name(project_id=project.project_id)
        #manage data
        texts = [chunk.chunk_text for chunk in processed_chunks]
        metadata = [chunk.chunk_metadata for chunk in processed_chunks]
        vectors= [
                self.embedding_client.embed_text(text=txt,document_type=DocumentTypeEnums.DOCUMENT.value)
                for txt in texts
        ]

        # create collection if not exists
        _=self.vector_db_client.create_collection(collection_name=collection_name, 
                                                           embedding_dimension=self.embedding_client.embedding_size, do_reset =False)

        # insert data into vector db
        _=self.vector_db_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadata,
            record_ids=chunks_ids,
        )


        return True
    def search_vector_db_collection(self,project:Project,text:str,limit:int=10):
        collection_name = self.create_collection_name(project_id=project.project_id)
        # get the collection name from the project id
        vectors= self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnums.QUERY.value)
        if not vectors or len(vectors) ==0:
            return False
        search_result = self.vector_db_client.search_by_vector(
                            collection_name=collection_name,
                            vector=vectors,
                            limit=limit,
            )
        return json.loads(
            json.dumps( search_result, default=lambda o: o.__dict__ ) 
        )
    