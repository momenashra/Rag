from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignals
from .ProjectController import ProjectController
import os
import re


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False, ResponseSignals.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignals.FILE_SIZE_EXCEEDEDD.value

        return True, ResponseSignals.FILE_UPLOAD_SUCCESS.value

    def generate_unique_filepath(self, project_id: str, original_file_name: str):
        random_file_name = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(
            original_file_name=original_file_name
        )
        new_file_path = os.path.join(
            project_path, random_file_name + "_" + cleaned_file_name
        )
        while os.path.exists(new_file_path):
            random_file_name = self.generate_random_string()
            cleaned_file_name = self.get_clean_file_name(
                original_file_name=original_file_name
            )
            new_file_path = os.path.join(
                project_path, random_file_name + "_" + cleaned_file_name
            )
        return new_file_path, random_file_name + "_" + cleaned_file_name

    def get_clean_file_name(self, original_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r"[^\w.]", "", original_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
