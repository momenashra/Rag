from .rag_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, func,Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID,JSONB
import uuid




class Asset(SQLAlchemyBase):
    __tablename__ = "assets" 

    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False)
    asset_config = Column(JSONB, nullable=True)
    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    project=relationship("Project", back_populates="assets")
    chunks=relationship("DataChunk", back_populates="asset")    
    summaries=relationship("Summary", back_populates="asset")

    __table_args__ = (
       Index('idx_asset_project_id', asset_project_id),
       Index('idx_asset_uuid', asset_uuid),
    )