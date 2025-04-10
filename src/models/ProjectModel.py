from .BaseDataModel import BaseDataModel
from .db_shemas import Project
from .enums.DataBaseEnum import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_clint=db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] #TAKE COLLECTION
        
    async def create_project(self, project: Project):
        result = await self.collection.insert_one(project.model_dump(by_alias=True, exclude_unset=True))
        # Check if the insertion was successful
        project._id = result.inserted_id  
        return project  # Return the created project with the assigned _id 

    async def get_project_or_create_one(self, project_id: str):
        record = await self.collection.find_one({"project_id": project_id})
        if record is None:
            # If the project doesn't exist, create a new one with the given project_id
            project = Project(project_id=project_id)
            project=await self.create_project(project)
            return project 

        return Project(**record)    # Return the existing project as a Project object
    async def get_all_projects(self,page:int =1,page_size : int = 10): # Get all projects from the collection and use pagination
        # Calculate the number of documents to skip based on the page and page size
        total_documents = await self.collection.count_documents({})
        #calculate the number of pages 
        total_pages =  total_documents  // page_size
        if total_documents % page_size != 0:
            total_pages += 1    
        cursor = self.collection.find().skip(page-1*page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))
        return {"projects": projects, "total_pages": total_pages, "current_page": page}  # Return the list of projects and pagination info

        
