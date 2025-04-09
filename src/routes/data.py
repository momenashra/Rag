from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
from models import ResponseSignals
import os
import aiofiles
import logging
from .schema.schema_data import ProcessRequest
app_logger= logging.getLogger("uvicorn.error")
data_router=APIRouter(
    prefix = "/api/v1/data",
    tags =  ["api_v1","data"],
)
data_controller=DataController()
@data_router.post("/upload/{project_id}")
async def upload_data ( project_id: str , file : UploadFile,
                        app_settings:Settings=Depends(get_settings)):

    is_valid,result_signal = data_controller.validate_uploaded_file(file=file)


    if not is_valid:
        return JSONResponse(  
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
                "signal" : result_signal
            }
          )

    projec_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path,file_id=  data_controller.generate_unique_filepath(project_id=project_id,original_file_name=file.filename)
  
    try:
        async with aiofiles.open (file_path,"wb") as f :
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write (chunk)
    except Exception as e :
        app_logger.error(f"error while uploading file:{e}")
        return JSONResponse( 
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = {
                    "signal" : ResponseSignals.FILE_UPLOAD_FAIL.value
            }
        )


    return JSONResponse(  
        content = {
            "signal" : ResponseSignals.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id
            }
        )


@data_router.post("/process/{project_id}")
async def process_endpoint ( project_id: str , process_request : ProcessRequest):
    file_id = process_request.file_id
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    processed_content=process_controller.process_file_content(file_content=file_content,file_id=file_id,
                                                              chunk_size=process_request.chunk_size,
                                                              overlap_size=process_request.overlap_size)


    if processed_content is None or len(processed_content)==0:
        return JSONResponse( 
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = {
                    "signal" : ResponseSignals.FILE_PROCESSING_FAIL.value
            }
        )
    return processed_content