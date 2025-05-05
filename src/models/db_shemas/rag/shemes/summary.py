from .rag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey,Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID,JSONB
import uuid
from pydantic import BaseModel


class Summary(SQLAlchemyBase):
    __tablename__ = "summaries" 

    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    summary_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    summary_text = Column(String, nullable=False)
    summary_metadata = Column(String, nullable=True)
    summary_order = Column(Integer, nullable=False)

    summary_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    summary_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)


    project=relationship("Project", back_populates="summaries")    
    asset=relationship("Asset", back_populates="summaries")

    __table_args__ = (
       Index('idx_summary_asset_id',summary_asset_id),
       Index('idx_summary_project_id', summary_project_id),
       Index('idx_summary_uuid', summary_uuid),
    )
class RetrivedData(BaseModel):
    text: str
    metadata: str