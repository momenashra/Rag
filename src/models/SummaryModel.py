from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func,delete
from bson import ObjectId
from models.db_shemas.rag.shemes import Summary
class SummaryModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_clint=db_client)
        self.db_client= db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client)
        return instance

    async def create_summary(self, summary: Summary):
        async with self.db_client() as session:
            async with session.begin():
                session.add(summary)
            await session.commit()
        return summary  
    
    async def get_summary(self, project_id: int):
        async with self.db_client() as session:
            async with session.begin():
                query = await session.execute(
                    select(Summary)
                    .where(Summary.summary_project_id == project_id)
                    .order_by(Summary.summary_order.desc())
                    .limit(1)
                )
                summary = query.scalar_one_or_none()
        return summary

    async def get_all_summaries(self, project_id: int):
        async with self.db_client() as session:
            async with session.begin():
                query = await session.execute(
                    select(Summary)
                    .where(Summary.summary_project_id == project_id)
                    .order_by(Summary.summary_order.desc())
                )
                summaries = query.scalars().all()
        return summaries

    async def insert_many_summaries(self, summaries: list, batch_size: int = 100):
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(summaries), batch_size):
                    batch = summaries[i : i + batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(summaries)  # Return the number of inserted summaries  

    async def delete_all_summaries_by_project_id(self, project_id: str):
        async with self.db_client() as session:
            async with session.begin():
                query = await session.execute (delete(Summary).where(Summary.summary_project_id == project_id))
                await session   .commit()
        return query.rowcount  # Return the number of deleted summaries
 