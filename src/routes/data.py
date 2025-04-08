from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers import get_settings,Settings
from controllers import DataController,ProjectController
from models import ResponseSignals
import os
import aiofiles
data_router=APIRouter(
    prefix = "/api/v1/data",
    tags =  ["api_v1","data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data ( project_id: str , file : UploadFile,
                        app_settings:Settings=Depends(get_settings)):

    is_valid,result_signal = DataController().validate_uploaded_file(file=file)


    if not is_valid:
        return JSONResponse(  
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : result_signal
            }
          )

    projec_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path= os.path.join (
        projec_dir_path,
        file.filename
    )

    async with aiofiles.open (file_path,"wb") as f :
        while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
            await f.write (chunk)

        return JSONResponse(  
            content = {
                "signal" : ResponseSignals.FILE_UPLOAD_SUCCESS.value
            }
          )
