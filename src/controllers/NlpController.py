from .BaseController import BaseController
from fastapi import HTTPException

from models.db_shemas import DataChunk, Project
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnums
import json
from models.db_shemas import RetrivedData

class NlpController(BaseController):
    def __init__(self,vector_db_client,embedding_client,generation_client,template_parser):
        super().__init__()
        self.vector_db_client = vector_db_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client
        self.template_parser = template_parser
        
    def create_collection_name(self,project_id:str):
        collection_name = f"collection_{self.vector_db_client.default_vector_size}_{project_id}"
        return collection_name
    

    async def reset_vector_db_collection(self, project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return  await self.vector_db_client.delete_collection(collection_name=collection_name)

    async def get_vector_db_collection_info(self, project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        print(f"[VectorDB] Getting collection info for {collection_name}")
        try:
            collection_info= await self.vector_db_client.get_collection_info(collection_name=collection_name)
        except ValueError as e:
            # Log if needed
            print(f"[VectorDB Error] {e}")
            # Return HTTP 404 instead of crashing
            raise HTTPException(status_code=404, detail=f"Collection '{collection_name}' not found")
        return json.loads(
            json.dumps( collection_info, default=lambda o: o.__dict__ ) 
        )
    
    async def index_into_vector_db (self,project:Project,processed_chunks:List [DataChunk],chunks_ids:list[int], do_reset:bool =False):

        # get the collection name from the project id
        collection_name = self.create_collection_name(project_id=project.project_id)
        #manage data
        texts = [chunk.chunk_text for chunk in processed_chunks]
        metadata = [chunk.chunk_metadata for chunk in processed_chunks]
        vectors=    self.embedding_client.embed_text(text=texts,document_type=DocumentTypeEnums.DOCUMENT.value)
        # create collection if not exists
        _=await self.vector_db_client.create_collection(collection_name=collection_name, 
                                                           embedding_dimension=self.embedding_client.embedding_size, do_reset =False)

        # insert data into vector db
        _= await self.vector_db_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadata,
            record_ids=chunks_ids,
        )
        return True
    
    async def search_vector_db_collection(self,project:Project,text:str,limit:int=10):
        collection_name = self.create_collection_name(project_id=project.project_id)
        query_vector = None
        # get the collection name from the project id
        vectors=  self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnums.QUERY.value)
        if not vectors or len(vectors) ==0:
            return False
        if isinstance(vectors, list) and len(vectors) > 0:
            # If the embedding is a list, use the first element
            query_vector = vectors[0]
        search_result =  await self.vector_db_client.search_by_vector(
                            collection_name=collection_name,
                            vector=query_vector,
                            limit=limit,
            )
        reranked_search_result =  self.embedding_client.rerank_search_result(query=text,documents=search_result)
        print(f"reranked_search_result is {reranked_search_result}")
        
    
    
        return [
            RetrivedData(
                text=record['document'],  # Using dictionary keys
                score=record['score']
            )
            for record in reranked_search_result
        ]


    async def answer_rag_questions(self,project:Project,query:str,limit:int=10):
        retrived_documents =await  self.search_vector_db_collection(project=project,text=query,limit=limit)
        answer,full_prompt,chat_history=None, None, None

        if not retrived_documents or len(retrived_documents) ==0:
            return answer,full_prompt,chat_history

        #construcrt the context for the LLM (query + retrived documents)
        system_prompt = self.template_parser.get(
            group="rag",
            key="system_prompt",
            )
    
        documents_prompts="\n".join([

            self.template_parser.get(group="rag",
                key="document_prompt",
                vars={
                    "doc_num": idx+1 ,
                    "chunk_text": doc.text
                }
            )
            for idx,doc in enumerate(retrived_documents)
        ])
        # summary_chain = self.generation_client.get_memory()
        # summary_text = summary_chain.memory.buffer  # get the actual summary    
        # summary_prompt = self.template_parser.get(group="rag",key="summary_prompt",vars={
        #     "summary": summary_text
        # })
        footer_prompt = self.template_parser.get(
            group="rag",
            key="footer_prompt",
            vars={
                "query": query,
            }
        )

        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role= self.generation_client.enums.SYSTEM.value
            )
        ]

        full_prompt="\n\n".join([documents_prompts,footer_prompt])

        answer=self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history,
            max_output_tokens=self.generation_client.default_max_output_tokens,
            temperature=self.generation_client.default_temperature
        )
        return answer,full_prompt,chat_history
    