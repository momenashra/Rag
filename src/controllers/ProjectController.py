from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignals
import os
class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
  
    def get_project_path (self,project_id:str):
        self.project_dir=os.path.join(
            self.file_dir,
            project_id
        )        
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)
        return self.project_dir