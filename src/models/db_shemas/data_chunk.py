from pydantic import BaseModel, validator, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class DataChunk(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId
    chunk_asset_id: ObjectId

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def get_indexes(cls):
        return [
            {
                "key": [("chunk_project_id", 1)],  # ascending order
                "name": "chunk_project_id_index_1",
                "unique": False,
            },
        ]

class RetrivedData(BaseModel):
    text: str
    score: float