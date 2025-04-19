from .BaseDataModel import BaseDataModel
from .db_shemas import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from pymongo import InsertOne


class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_clint=db_client)
        self.collection = self.db_client[
            DataBaseEnum.COLLECTION_CHUNK_NAME.value
        ]  # TAKE COLLECTION

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        # Check if the collection already exists
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            # Create the collection
            self.collection = self.collection = self.db_client[
                DataBaseEnum.COLLECTION_CHUNK_NAME.value
            ]
            # Create indexes for the collection
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"], name=index["name"], unique=index["unique"]
                )

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(
            chunk.model_dump(by_alias=True, exclude_unset=True)
        )
        # Check if the insertion was successful
        chunk._id = result.inserted_id
        return chunk  # Return the created chunk with the assigned _id

    async def get_chunk(self, chunk_id: str):
        record = await self.collection.find_one({"chunk_id": ObjectId(chunk_id)})
        if record is None:
            return None

        return DataChunk(**record)  # Return the existing Chunk as a Chunk object

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        # Split the chunks into batches of the specified size
        for c in range(0, len(chunks), batch_size):
            chunk_batch = chunks[c : c + batch_size]
            # Bulk write
            operation = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True))
                for chunk in chunk_batch
            ]
            await self.collection.bulk_write(operation)
        return len(chunks)  # Return the number of inserted chunks

    async def delete_all_chunks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({"chunk_project_id": (project_id)})
        return result.deleted_count


    async def get_all_project_chunks_by_project_id(self, project_id: ObjectId,page_no:int=1,page_size:int=50):

        records = await self.collection.find( 
                    {"chunk_project_id": project_id}
             ).skip((page_no - 1) * page_size).limit(page_size).to_list(length=None)

        return [
            DataChunk(**record) 
            for record in records
        ]