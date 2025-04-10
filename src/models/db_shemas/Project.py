from pydantic import BaseModel,validator, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class Project (BaseModel):

    id : Optional[ObjectId] = Field(None, alias="_id")
    project_id :str = Field(..., min_length=1, max_length=100)

    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
