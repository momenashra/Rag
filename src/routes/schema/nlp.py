from pydantic import BaseModel
from typing import Optional


class PushRequest(BaseModel):
    do_reset: Optional[int] = 0


class SearchRequest(BaseModel):
    text: str 
    limit: Optional[int] = 10


class AnswerRequest(BaseModel):
    query: str 
    limit: Optional[int] = 10


