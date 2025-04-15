from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from helpers import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
from models import ResponseSignals
import os
import aiofiles
import logging
from .schema.schema_data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_shemas import DataChunk ,Asset
from models.AssetModel import AssetModel
from models.enums.AssetTypeEnum import AssetTypeEnum
app_logger= logging.getLogger("uvicorn.error")

data_router=APIRouter(
    prefix = "/api/v1/data",
    tags =  ["api_v1","data"],
)

# Initialize the DataController instance
# Initialize the ProjectModel instance
data_controller=DataController()
@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id: str , file : UploadFile,
                        app_settings:Settings=Depends(get_settings)):
    project_model=await ProjectModel.create_instance(db_client=request.app.mongo_db)
    # Check if the project exists in the database
    project = await project_model.get_project_or_create_one(project_id=project_id)

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
    # store asset in the database   
    asset_model=await AssetModel.create_instance(db_client=request.app.mongo_db)
    asset_resource=Asset(
        asset_project_id=project.id,
        asset_name=file_id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_size=os.path.getsize(file_path),
        asset_config={
            "file_path": file_path,
            "file_id": file_id,
            "file_name": file.filename,
            "file_type": file.content_type,
        }
    )
    # Check if the asset already exists in the database
    asset_record= await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(  
        content = {
            "signal" : ResponseSignals.FILE_UPLOAD_SUCCESS.value,
            "file_id": str(asset_record.id),
            "project_id": str(project.id)
            }
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id: str , process_request : ProcessRequest):
    project_model=await ProjectModel.create_instance(db_client=request.app.mongo_db)
    # Check if the project exists in the database
    project = await project_model.get_project_or_create_one(project_id=project_id)
    process_controller=ProcessController(project_id=project_id)

    project_file_ids={}
    if process_request.file_id :

        asset_model=await AssetModel.create_instance(db_client=request.app.mongo_db)
        asset_record= await asset_model.get_asset(asset_project_id=project.id,asset_name=process_request.file_id)
        if asset_record is None:
            return JSONResponse( 
                status_code = status.HTTP_400_BAD_REQUEST, 
                content = {
                        "signal" : ResponseSignals.FILE_NOT_FOUND.value
                }
            )
        else:
            project_file_ids={
                asset_record.id:asset_record.asset_name
            }
    else:
        asset_model=await AssetModel.create_instance(db_client=request.app.mongo_db)
        project_files=await asset_model.get_all_project_assets(asset_project_id=project.id,asset_type=AssetTypeEnum.FILE.value)
        project_file_ids={
            record.id:record.asset_name
            for record in project_files 
        }
    if len(project_file_ids)==0:
        return JSONResponse( 
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = {
                    "signal" : ResponseSignals.NO_FILES_ERROR.value
            }
        )
    inserted_count=0
    no_files=0
    chunk_model=await ChunkModel.create_instance(db_client=request.app.mongo_db)
    if process_request.do_reset ==1:
        _ = await chunk_model.delete_all_chunks_by_project_id(project_id=(project.id))

    for asset_id,file_id in project_file_ids.items():

        file_content=process_controller.get_file_content(file_id=file_id)
        if file_content is None:
            app_logger.error(f"error while processing file:{file_id} not found")
            continue
        processed_chunks=process_controller.process_file_content(file_content=file_content,file_id=file_id,
                                                                chunk_size=process_request.chunk_size,
                                                                overlap_size=process_request.overlap_size)

        if processed_chunks is None or len(processed_chunks)==0:
            return JSONResponse( 
                status_code = status.HTTP_400_BAD_REQUEST, 
                content = {
                        "signal" : ResponseSignals.FILE_PROCESSING_FAIL.value
                }
            )
        
        processed_chunks_records=[
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i,chunk in enumerate(processed_chunks)
        ]

        # Insert the processed chunks into the database
        inserted_count += await chunk_model.insert_many_chunks(chunks=processed_chunks_records)
        no_files += 1
    if inserted_count == 0:
        return JSONResponse( 
            status_code = status.HTTP_400_BAD_REQUEST, 
            content = {
                    "signal" : ResponseSignals.FILE_PROCESSING_FAIL.value
            }
        )
    else:
        return JSONResponse(  
            content = {
                "signal" : ResponseSignals.FILE_PROCESSING_SUCCESS.value,
                "inserted_chunks_count": inserted_count,
                "processed_files_count": no_files,
                }
            )





