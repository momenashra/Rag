from .rag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, func,Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID,JSONB
import uuid
from pydantic import BaseModel


class DataChunk(SQLAlchemyBase):
    __tablename__ = "chunks" 

    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=True)
    chunk_order = Column(Integer, nullable=False)

    chunk_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    chunk_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)

    created_at = Column(DateTime(timezone=True),server_default=func.now() ,nullable=False)
    updated_at = Column(DateTime(timezone=True),onupdate=func.now() ,nullable=True)

    project=relationship("Project", back_populates="chunks")    
    asset=relationship("Asset", back_populates="chunks")

    __table_args__ = (
       Index('idx_chunk_asset_id',chunk_asset_id),
       Index('idx_chunk_project_id', chunk_project_id),
       Index('idx_chunk_uuid', chunk_uuid),
    )
class RetrivedData(BaseModel):
    text: str
    score: float