from .BaseDataModel import BaseDataModel
from .db_shemas import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func,delete
from bson import ObjectId
class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_clint=db_client)
        self.db_client= db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client)
        return instance

    async def create_chunk(self, chunk: DataChunk):
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
        return chunk  
    
    async def get_chunk(self, chunk_id: str):
        async with self.db_client() as session:
            async with session.begin():
                query = await session.execute (select(DataChunk).where(DataChunk.chunk_id == chunk_id))
                chunk = query.scalar_one_or_none()
        return chunk


    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i : i + batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(chunks)  # Return the number of inserted chunks  

    async def delete_all_chunks_by_project_id(self, project_id: str):
        async with self.db_client() as session:
            async with session.begin():
                query = await session.execute (delete(DataChunk).where(DataChunk.chunk_project_id == project_id))
                await session   .commit()
        return query.rowcount  # Return the number of deleted chunks
 

    async def get_all_project_chunks_by_project_id(self, project_id: ObjectId,page_no:int=1,page_size:int=50):

        async with self.db_client() as session:
            async with session.begin():
                query =await session.execute (select(DataChunk).where(DataChunk.chunk_project_id == project_id))
                records= query.scalars().all()
            return records
    
    async def get_total_chunks_count(self, project_id: ObjectId):
        records_count=0
        async with self.db_client() as session:
            async with session.begin():
                count_query = await session.execute (select(func.count(DataChunk.chunk_id)).where(DataChunk.chunk_project_id == project_id))
                records_count= count_query.scalar()
        return records_count
    